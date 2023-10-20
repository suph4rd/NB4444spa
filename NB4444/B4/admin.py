from django.contrib import admin
from django.utils.safestring import mark_safe

from B4 import models, mixins, admin_filters


@admin.register(models.Note)
class NoteAdmin(mixins.AdminQsManagerMixin, mixins.AdminDeleteActionMixin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'is_delete', 'user', 'text', 'get_image')
    list_display_links = ('id', 'created_at')
    search_fields = ('created_at', 'text')
    list_filter = ('is_delete', admin_filters.NoteImageExistFilter, admin_filters.NoteTextExistFilter)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" >') if obj.image else 'Фото отсутствует'
    get_image.short_description = "Фото"


@admin.register(models.Plan)
class PlanAdmin(mixins.AdminQsManagerMixin, mixins.AdminDeleteActionMixin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'name', 'user', 'is_delete')
    list_display_links = ('id', 'created_at')
    list_filter = ('is_delete', )


@admin.register(models.Task)
class TaskAdmin(mixins.AdminQsManagerMixin, mixins.AdminDeleteActionMixin, admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'is_delete', 'plan', 'section', 'description', 'is_ready', 'priority')
    list_display_links = ('id', 'created_at')
    list_filter = ('is_delete',)


@admin.register(models.DefaultDeductions)
class DefaultDeductionsAdmin(mixins.AdminQsManagerMixin, mixins.AdminDeleteActionMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'is_delete')
    list_display_links = ('id',)
    list_filter = ('is_delete', )


@admin.register(models.User)
class UserAdmin(mixins.AdminQsManagerMixin, admin.ModelAdmin):
    list_display = ('id', 'username', 'get_full_name', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    def save_model(self, request, obj, form, change):
        check_field = "password"
        if check_field in form.changed_data:
            obj.set_password(form.cleaned_data.get(check_field))
        super().save_model(request, obj, form, change)


admin.site.register(models.Section)
