from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock

from rest_framework.exceptions import ValidationError

from .services import (
    NoteQuerysetFilterService,
    PlanQuerysetFilterService,
    QuerysetFilterService,
    TaskQuerysetFilterService,
)


class QuerysetFilterServiceTests(TestCase):
    def setUp(self):
        self.queryset = Mock()
        self.queryset.filter.return_value = self.queryset
        self.user = SimpleNamespace(is_authenticated=True, is_superuser=False)

    def apply(self, service, params=None):
        return service.filter_queryset(self.queryset, self.user, params or {})

    def test_anonymous_user_gets_empty_queryset_without_validation(self):
        self.user.is_authenticated = False
        result = self.apply(TaskQuerysetFilterService(), {'is_ready': 'invalid'})
        self.assertIs(result, self.queryset.none.return_value)
        self.queryset.filter.assert_not_called()

    def test_owner_field_and_search_follow_service_type(self):
        for service, owner, field in (
            (QuerysetFilterService(), 'user', None),
            (NoteQuerysetFilterService(), 'user', 'text'),
            (PlanQuerysetFilterService(), 'user', 'name'),
            (TaskQuerysetFilterService(), 'plan__user', 'description'),
        ):
            with self.subTest(service=type(service).__name__):
                self.queryset.reset_mock()
                self.assertIs(self.apply(service, {'search': 'sample'}), self.queryset)
                self.queryset.filter.assert_any_call(**{owner: self.user})
                searches = [call.kwargs for call in self.queryset.filter.call_args_list
                            if any(key.endswith('__icontains') for key in call.kwargs)]
                self.assertEqual(searches, [{field + '__icontains': 'sample'}] if field else [])

    def test_superuser_still_gets_task_search_and_deleted_plan_filter(self):
        self.user.is_superuser = True
        self.apply(TaskQuerysetFilterService(), {'search': 'sample'})
        self.assertEqual(self.queryset.filter.call_count, 2)
        self.queryset.filter.assert_any_call(description__icontains='sample')
        self.queryset.filter.assert_any_call(plan__is_delete=False)

    def test_task_filters_and_boolean_conversion(self):
        for value, expected in (('true', True), ('false', False)):
            self.apply(TaskQuerysetFilterService(), {
                'plan': '1', 'section': '2', 'priority': '3', 'is_ready': value,
            })
            for key, item in (('plan', 1), ('section', 2), ('priority', 3),
                              ('is_ready', expected)):
                self.queryset.filter.assert_any_call(**{key: item})

    def test_invalid_ready_value_preserves_validation_error(self):
        with self.assertRaises(ValidationError) as error:
            self.apply(TaskQuerysetFilterService(), {'is_ready': 'True'})
        self.assertEqual(str(error.exception.detail['is_ready']), 'Ожидается true или false')
