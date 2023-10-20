import copy

from rest_framework import status
from rest_framework.response import Response


class ListFilterMixin:
    def get_int_value(self, value) -> int:
        match value:
            case int(value):
                return value
            case str(value) if value.isdigit() :
                return int(value)
            case list(value) if len(value) == 1:
                return self.get_int_value(value[0])
        raise ValueError({"error": f"{value} is not convent to Integer"})

    def list(self, request, *args, **kwargs):
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
        if offset or limit:
            try:
                int_offset = self.get_int_value(offset)
                int_limit = self.get_int_value(limit)
                if int_offset and int_limit and int_offset >= int_limit:
                    raise ValueError(f"offset: {offset} больше либо равен limit: {limit}")
                self.queryset = self.queryset[int_offset: int_limit]
            except Exception as err:
                print(err)
                return Response({"statusText": str(err)}, status=400)
        return super().list(request, *args, **kwargs)


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
        data = copy.deepcopy(request.data)
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CRWithUserMixin(ListWithUserMixin, CreateWithUserMixin):
    pass
