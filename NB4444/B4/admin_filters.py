from django.contrib import admin
from django.db.models import Q
from django.db.models.functions import Trim


class ExistFilterBase(admin.SimpleListFilter):
    model_param = None

    def __init__(self, *args, **kwargs):
        if not self.model_param:
            raise ValueError("model_param is required!")
        super(ExistFilterBase, self).__init__(*args, **kwargs)

    def lookups(self, request, model_admin):
        return (
            ("true", "Да"),
            ("false", "Нет"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val in ("true", "false"):
            queryset = queryset.annotate(looking_field=Trim(self.model_param))
            val = val == "true"
            filter_params = (Q(**{f"{self.model_param}__isnull": True}) | Q(**{"looking_field": ''}))
            if val:
                filter_params = (Q(**{f"{self.model_param}__isnull": False}) & ~Q(**{"looking_field": ''}))
            queryset = queryset.filter(filter_params)
        return queryset


class NoteImageExistFilter(ExistFilterBase):
    title = 'Наличие фото'
    parameter_name = 'image_exist'
    model_param = 'image'


class NoteTextExistFilter(ExistFilterBase):
    title = 'Наличие текста'
    parameter_name = 'text_exist'
    model_param = 'text'
