from rest_framework import status
from rest_framework.response import Response

from .services import QuerysetFilterService


class ListFilterMixin:
    queryset_filter_service_class = QuerysetFilterService

    def get_queryset(self):
        return self.queryset_filter_service_class().filter_queryset(
            queryset=super().get_queryset(),
            user=self.request.user,
            query_params=self.request.query_params,
        )

    def list(self, request, *args, **kwargs):
        from rest_framework.exceptions import ValidationError
        qs = self.filter_queryset(self.get_queryset())
        try:
            offset = int(request.GET.get('offset', 0))
            limit = request.GET.get('limit')
            limit = int(limit) if limit is not None else None
            if offset < 0 or (limit is not None and limit < offset):
                raise ValueError()
        except (ValueError, TypeError):
            raise ValidationError('Некорректные границы списка')
        return Response(self.get_serializer(qs[offset:limit], many=True).data)


class ListWithUserMixin:
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"statusText": "Пользователь не авторизован!"}, status=403)
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)


class CreateWithUserMixin:
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"statusText": "Пользователь не авторизован!"}, status=403)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CRWithUserMixin(ListWithUserMixin, CreateWithUserMixin):
    pass
