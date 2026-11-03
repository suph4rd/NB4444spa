def register_resources(mcp):

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
