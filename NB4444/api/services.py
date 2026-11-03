from rest_framework.exceptions import ValidationError


class QuerysetFilterService:
    owner_field = 'user'
    search_field = None

    def filter_queryset(self, queryset, user, query_params):
        if not user.is_authenticated:
            return queryset.none()
        if not user.is_superuser:
            queryset = queryset.filter(**{self.owner_field: user})
        search = query_params.get('search')
        if search and self.search_field:
            queryset = queryset.filter(**{self.search_field + '__icontains': search})
        return self.filter_additional(queryset, query_params)

    def filter_additional(self, queryset, query_params):
        return queryset


class NoteQuerysetFilterService(QuerysetFilterService):
    search_field = 'text'

    def filter_additional(self, queryset, query_params):
        value = query_params.get('has_image')
        if value is None:
            return queryset
        if value not in ('true', 'false'):
            raise ValidationError({'has_image': 'Ожидается true или false'})
        if value == 'true':
            return queryset.exclude(image='').exclude(image__isnull=True)
        from django.db.models import Q
        return queryset.filter(Q(image='') | Q(image__isnull=True))


class PlanQuerysetFilterService(QuerysetFilterService):
    search_field = 'name'


class TaskQuerysetFilterService(QuerysetFilterService):
    owner_field = 'plan__user'
    search_field = 'description'

    def filter_additional(self, queryset, query_params):
        queryset = queryset.filter(plan__is_delete=False)
        for key in ('plan', 'section', 'priority', 'is_ready'):
            value = query_params.get(key)
            if value is not None:
                if key == 'is_ready':
                    if value not in ('true', 'false'):
                        raise ValidationError({key: 'Ожидается true или false'})
                    value = value == 'true'
                else:
                    try:
                        value = int(value)
                    except (TypeError, ValueError):
                        raise ValidationError({key: 'Ожидается целое число'})
                queryset = queryset.filter(**{key: value})
        return queryset
