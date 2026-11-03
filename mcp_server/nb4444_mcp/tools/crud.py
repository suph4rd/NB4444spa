from typing import Annotated

from pydantic import Field


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


def register_entity(mcp, api_client, entity, endpoint):
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
        rows = api_client.read_json(api_client.request('GET', path, params=params))
        if not isinstance(rows, list):
            raise ValueError('api_unavailable: ожидался список')
        return {'items': rows[:page_size], 'next_offset': offset + page_size if len(rows) > page_size else None}

    def get(id: int) -> dict:
        return api_client.read_json(api_client.request('GET', path + f'{id}/'))

    def create(data: dict) -> dict:
        validate_fields(data)
        return api_client.read_json(api_client.request('POST', path, json=data))

    def update(id: int, data: dict) -> dict:
        validate_fields(data)
        return api_client.read_json(api_client.request('PATCH', path + f'{id}/', json=data))

    def delete(id: int) -> dict:
        api_client.request('DELETE', path + f'{id}/')
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


def register_crud(mcp, api_client):
    for entity, endpoint in [('notes', 'note'), ('plans', 'plan'), ('tasks', 'task'),
                             ('deductions', 'default-deduction')]:
        register_entity(mcp, api_client, entity, endpoint)
