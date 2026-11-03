def register_prompts(mcp):

    @mcp.prompt()
    def review_plan(plan_id: int) -> str:
        return f'Прочитай план {plan_id} и его задачи, оцени прогресс и предложи следующие действия.'

    @mcp.prompt()
    def summarize_notes(search: str = '') -> str:
        return f'Найди заметки по запросу {search!r}, прочитай все страницы и составь сводку.'
