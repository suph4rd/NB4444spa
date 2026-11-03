import os
import logging
from pathlib import Path
from typing import Annotated

from pydantic import Field

import httpx
from mcp.server.fastmcp import FastMCP, Image

mcp = FastMCP('NB4444')
base = os.environ.get('NB4444_API_URL', 'http://localhost:8008').rstrip('/')
token = os.environ.get('NB4444_ACCESS_TOKEN', '')
client = httpx.Client(timeout=float(os.environ.get('NB4444_HTTP_TIMEOUT', '30')))


MAX_IMAGE_SIZE = 10 * 1024 * 1024


def request(method, path, **kwargs):
    global token
    stream = kwargs.pop('stream', False)

    def send():
        req = client.build_request(method, base + path,
                                   headers={'Authorization': 'Bearer ' + token}, **kwargs)
        return client.send(req, stream=stream)

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
            refresh = client.post(base + '/auth/jwt/refresh/',
                                  json={'refresh': os.environ.get('NB4444_REFRESH_TOKEN', '')})
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
            token = access
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


def read_json(response):
    try:
        return response.json()
    except ValueError:
        raise ValueError('api_unavailable: некорректный JSON ответа') from None


ENTITY_FIELDS = {
    'notes': {'text': {'type': ['string', 'null']}, 'image': {'type': 'null'}},
    'plans': {'name': {'type': 'string', 'maxLength': 255}},
    'tasks': {
        'plan': {'type': 'integer'}, 'section': {'type': ['integer', 'null']},
        'description': {'type': 'string'}, 'is_ready': {'type': 'boolean'},
        'priority': {'type': 'integer', 'minimum': 0, 'maximum': 3},
    },
    'deductions': {key: {'type': 'string', 'description': 'Десятичная денежная сумма'}
                   for key in ('house', 'travel', 'phone', 'food')},
}


def register(entity, endpoint):
    path = '/api/v1/' + endpoint + '/'

    def listing(
        offset: int = 0, page_size: int = 20, search: str = '',
        plan: int | None = None, section: int | None = None,
        priority: int | None = None, is_ready: bool | None = None,
        has_image: bool | None = None,
    ) -> dict:
        if offset < 0 or not 1 <= page_size <= 100:
            raise ValueError('validation_error: неверная пагинация')
        if entity != 'tasks' and any(v is not None for v in (plan, section, priority, is_ready)):
            raise ValueError('validation_error: фильтры задач недоступны для этой сущности')
        if has_image is not None and entity != 'notes':
            raise ValueError('validation_error: has_image доступен только для заметок')
        if entity == 'deductions' and search:
            raise ValueError('validation_error: поиск по вычетам недоступен')
        params = dict(offset=offset, limit=offset + page_size + 1, search=search)
        for key, value in dict(plan=plan, section=section, priority=priority, is_ready=is_ready).items():
            if value is not None:
                params[key] = str(value).lower()
        if has_image is not None:
            params['has_image'] = str(has_image).lower()
        rows = read_json(request('GET', path, params=params))
        if not isinstance(rows, list):
            raise ValueError('api_unavailable: ожидался список')
        return {'items': rows[:page_size], 'next_offset': offset + page_size if len(rows) > page_size else None}

    def get(id: int) -> dict:
        return read_json(request('GET', path + f'{id}/'))

    def create(data: dict) -> dict:
        validate_fields(data)
        return read_json(request('POST', path, json=data))

    def update(id: int, data: dict) -> dict:
        validate_fields(data)
        return read_json(request('PATCH', path + f'{id}/', json=data))

    def delete(id: int) -> dict:
        request('DELETE', path + f'{id}/')
        return {'deleted': True, 'id': id}

    def validate_fields(data):
        unknown = set(data) - ENTITY_FIELDS[entity].keys()
        if unknown:
            raise ValueError('validation_error: неизвестные поля: ' + ', '.join(sorted(unknown)))

    payload_type = Annotated[dict, Field(json_schema_extra={
        'properties': ENTITY_FIELDS[entity], 'additionalProperties': False,
    })]
    create.__annotations__['data'] = payload_type
    update.__annotations__['data'] = payload_type

    for prefix, fn in [('list', listing), ('get', get), ('create', create), ('update', update), ('delete', delete)]:
        fields = ', '.join(ENTITY_FIELDS[entity])
        description = f'{prefix} {entity}. Поля data: {fields}. '
        description += 'Списки: offset/page_size (1–100), search. '
        if entity == 'tasks':
            description += 'Фильтры: plan, section, priority (0–3), is_ready.'
        elif entity == 'notes':
            description += 'Фильтр: has_image. Для загрузки фото используйте set_note_image.'
        elif entity == 'deductions':
            description += 'Денежные значения: десятичные строки. Поиск не поддерживается.'
        mcp.tool(name=f'{prefix}_{entity if prefix == "list" else entity.rstrip("s")}',
                 description=description)(fn)


for entity, endpoint in [('notes', 'note'), ('plans', 'plan'), ('tasks', 'task'), ('deductions', 'default-deduction')]:
    register(entity, endpoint)


@mcp.tool(description='Текущий авторизованный пользователь: id и username.')
def get_current_user() -> dict:
    return read_json(request('GET', '/api/v1/user/current_user/'))


@mcp.tool(description='Доступные активные разделы: id и name.')
def list_sections() -> list:
    return read_json(request('GET', '/api/v1/section-list/'))


@mcp.tool(description='Последние вычеты текущего пользователя; 404, если отсутствуют.')
def get_latest_deductions() -> dict:
    return read_json(request('GET', '/api/v1/default-deduction/user_last/'))


@mcp.tool(description='Загрузить JPEG/PNG/WebP до 10 МиБ из NB4444_UPLOAD_ROOT в заметку.')
def set_note_image(id: int, path: str) -> dict:
    from PIL import Image as PILImage
    upload_root = os.environ.get('NB4444_UPLOAD_ROOT')
    if not upload_root:
        raise ValueError('validation_error: NB4444_UPLOAD_ROOT не настроен')
    try:
        root = Path(upload_root).resolve()
        source = Path(path).resolve()
        if (not source.is_relative_to(root) or not source.is_file()
                or source.stat().st_size > MAX_IMAGE_SIZE):
            raise ValueError('validation_error: недопустимый файл')
        with PILImage.open(source) as img:
            if img.format not in ('JPEG', 'PNG', 'WEBP'):
                raise ValueError('validation_error: формат изображения')
            img.verify()
        with source.open('rb') as file:
            return read_json(request('PATCH', f'/api/v1/note/{id}/',
                                     files={'image': (source.name, file)}))
    except (OSError, SyntaxError, PILImage.DecompressionBombError) as error:
        raise ValueError('validation_error: файл недоступен или повреждён') from error


@mcp.tool(description='Удалить связь заметки с фотографией.')
def remove_note_image(id: int) -> dict:
    return read_json(request('PATCH', f'/api/v1/note/{id}/', json={'image': None}))


@mcp.tool(description='Получить фотографию доступной заметки, максимум 10 МиБ.')
def get_note_image(id: int) -> Image:
    from io import BytesIO
    from PIL import Image as PILImage
    response = request('GET', f'/api/v1/note/{id}/image/', stream=True)
    try:
        data = bytearray()
        for chunk in response.iter_bytes(chunk_size=65536):
            if len(data) + len(chunk) > MAX_IMAGE_SIZE:
                raise ValueError('validation_error: слишком большое изображение')
            data.extend(chunk)
        try:
            with PILImage.open(BytesIO(data)) as img:
                image_format = img.format
                if image_format not in ('JPEG', 'PNG', 'WEBP'):
                    raise ValueError('validation_error: формат изображения')
                img.verify()
        except (OSError, SyntaxError, PILImage.DecompressionBombError) as error:
            raise ValueError('validation_error: повреждённое изображение') from error
        return Image(data=bytes(data), format=image_format.lower())
    except httpx.HTTPError:
        raise ValueError('api_unavailable: ошибка скачивания изображения') from None
    finally:
        response.close()


@mcp.tool(description='Случайные уникальные доступные заметки с фотографиями; count от 1 до 100.')
def get_random_notes_with_images(count: int = 10) -> dict:
    import random
    if not 1 <= count <= 100:
        raise ValueError('validation_error: count должен быть от 1 до 100')
    items = {}
    offset = 0
    while True:
        rows = read_json(request('GET', '/api/v1/note/',
                         params={'offset': offset, 'limit': offset + 100, 'has_image': 'true'}))
        if not isinstance(rows, list):
            raise ValueError('api_unavailable: ожидался список')
        for row in rows:
            if row.get('image'):
                items[row['id']] = row
        if len(rows) < 100:
            break
        offset += 100
    return {'items': random.sample(list(items.values()), min(count, len(items)))}


@mcp.resource('nb4444://guide')
def guide() -> str:
    return (
        'Заметки: text, image. Планы: name. '
        'Задачи: plan, section, description, is_ready, priority (0–3). '
        'Вычеты: house, travel, phone, food — десятичные строки. '
        'Удаление мягкое. Списки: offset/page_size. '
        'Заметки: has_image; случайная выборка: get_random_notes_with_images. '
        'Фото загружаются из NB4444_UPLOAD_ROOT.'
    )


@mcp.prompt()
def review_plan(plan_id: int) -> str:
    return f'Прочитай план {plan_id} и его задачи, оцени прогресс и предложи следующие действия.'


@mcp.prompt()
def summarize_notes(search: str = '') -> str:
    return f'Найди заметки по запросу {search!r}, прочитай все страницы и составь сводку.'


if __name__ == '__main__':
    logging.basicConfig()
    mcp.run(transport='stdio')
