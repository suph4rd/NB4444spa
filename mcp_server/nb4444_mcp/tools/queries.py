def register_queries(mcp, api_client):

    @mcp.tool(description='Текущий авторизованный пользователь: id и username.')
    def get_current_user() -> dict:
        return api_client.read_json(api_client.request('GET', '/api/v1/user/current_user/'))

    @mcp.tool(description='Доступные активные разделы: id и name.')
    def list_sections() -> list:
        return api_client.read_json(api_client.request('GET', '/api/v1/section-list/'))

    @mcp.tool(description='Последние вычеты текущего пользователя; 404, если отсутствуют.')
    def get_latest_deductions() -> dict:
        return api_client.read_json(api_client.request('GET', '/api/v1/default-deduction/user_last/'))


def register_random_query(mcp, api_client):

    @mcp.tool(description='Случайные уникальные доступные заметки с фотографиями; count от 1 до 100.')
    def get_random_notes_with_images(count: int = 10) -> dict:
        import random
        if not 1 <= count <= 100:
            raise ValueError('validation_error: count должен быть от 1 до 100')
        items = {}
        offset = 0
        while True:
            rows = api_client.read_json(api_client.request('GET', '/api/v1/note/',
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
