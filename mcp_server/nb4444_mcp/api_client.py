import httpx

from .settings import ServerSettings


class NB4444ApiClient:

    def __init__(self, settings: ServerSettings, client: httpx.Client | None = None):
        self.base = settings.api_url.rstrip('/')
        self.token = settings.access_token
        self.refresh_token = settings.refresh_token
        self.client = client if client is not None else httpx.Client(timeout=settings.http_timeout)

    def close(self):
        self.client.close()

    def request(self, method, path, **kwargs):
        stream = kwargs.pop('stream', False)

        def send():
            req = self.client.build_request(method, self.base + path,
                                       headers={'Authorization': 'Bearer ' + self.token}, **kwargs)
            return self.client.send(req, stream=stream)

        try:
            response = send()
            invalid_token = False
            if response.status_code == 403:
                response.read()
                try:
                    error = response.json()
                except ValueError:
                    error = None
                invalid_token = isinstance(error, dict) and error.get('code') == 'token_not_valid'
            if response.status_code == 401 or invalid_token:
                response.close()
                refresh = self.client.post(self.base + '/auth/jwt/refresh/',
                                      json={'refresh': self.refresh_token})
                if refresh.status_code >= 500 or refresh.status_code == 429:
                    raise ValueError('api_unavailable: сервис обновления JWT недоступен')
                if refresh.status_code != 200:
                    raise ValueError('authentication_required: обновите JWT и перезапустите MCP')
                try:
                    access = refresh.json()['access']
                    if not isinstance(access, str) or not access:
                        raise ValueError()
                except (ValueError, KeyError, TypeError):
                    raise ValueError('api_unavailable: некорректный ответ обновления JWT') from None
                self.token = access
                response = send()
            if response.is_error:
                code = {401: 'authentication_required', 403: 'permission_denied',
                        404: 'not_found', 400: 'validation_error'}.get(
                            response.status_code, 'api_unavailable')
                details = ''
                if response.status_code == 400:
                    response.read()
                    try:
                        details = ': ' + str(response.json())
                    except ValueError:
                        pass
                response.close()
                raise ValueError(f'{code}: HTTP {response.status_code}{details}')
            return response
        except httpx.HTTPError:
            suffix = '; результат записи может быть неизвестен' if method != 'GET' else ''
            raise ValueError('api_unavailable: ошибка соединения' + suffix) from None

    @staticmethod
    def read_json(response):
        try:
            return response.json()
        except ValueError:
            raise ValueError('api_unavailable: некорректный JSON ответа') from None

