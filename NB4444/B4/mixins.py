

class AdminQsManagerMixin:
    def get_queryset(self, request):
        manager = self.model._default_manager
        if hasattr(self.model, "get_admin_manager"):
            manager = self.model.get_admin_manager()
        qs = manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


class AdminDeleteActionMixin:
    actions = ("set_delete_status",)

    def set_delete_status(self, request, queryset):
        queryset.update(is_delete=True)

    set_delete_status.short_description = "Пометить как удалённые"
