import threading

from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import serializers
from api.mixins import CRWithUserMixin, ListFilterMixin
from api.permissions import IsSuperUserOrOwnerPermission
from B4 import models as b4_models


@api_view(['GET'])
def get_bot_info_view(request):
    from tele_bot import main
    t1 = threading.Thread(target=main.receive_records_from_telegramm_bot)
    t1.start()
    return Response(status=status.HTTP_200_OK)


class DefaultDeductionListFilterModelViewSet(ListFilterMixin, ModelViewSet):
    queryset = b4_models.DefaultDeductions.objects.all()
    serializer_class = serializers.get_model_serializer_class(
        b4_models.DefaultDeductions,
        local_exclude=['created_at', 'updated_at', 'delete_datetime', 'is_delete']
    )
    permission_classes = [IsSuperUserOrOwnerPermission]

    @action(methods=['get'], detail=False)
    def last(self, request, *args, **kwargs):
        qs = self.queryset.last()
        serializer = self.serializer_class(qs)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def user_last(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Пользователь не авторизован!"}, status=403)
        obj = self.queryset.filter(user=request.user).last()
        if not obj:
            return Response({}, status=404)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class PlanModelListFilterModelViewSet(ListFilterMixin, CRWithUserMixin, ModelViewSet):
    model = b4_models.Plan
    queryset = model.objects.all()
    serializer_class = serializers.get_model_serializer_class(
        b4_models.Plan,
        local_exclude=['created_at', 'updated_at', 'delete_datetime', 'is_delete']
    )
    permission_classes = [IsSuperUserOrOwnerPermission]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.DetailPlanSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ListPlanSerializer
        return super().list(request, *args, **kwargs)


class TaskModelListFilterModelViewSet(ListFilterMixin, ModelViewSet):
    model = b4_models.Task
    queryset = model.objects.all()
    serializer_class = serializers.get_model_serializer_class(
        b4_models.Task,
        local_exclude=['created_at', 'updated_at', 'delete_datetime', 'is_delete']
    )
    permission_classes = [IsSuperUserOrOwnerPermission]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.ListTaskSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ListTaskSerializer
        return super().list(request, *args, **kwargs)


class NoteModelListFilterModelViewSet(ListFilterMixin, CRWithUserMixin, ModelViewSet):
    model = b4_models.Note
    queryset = model.objects.all()
    permission_classes = [IsSuperUserOrOwnerPermission]
    serializer_class = serializers.get_model_serializer_class(
        b4_models.Note,
        local_exclude=['created_at', 'updated_at', 'delete_datetime', 'is_delete']
    )

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.ListNoteSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ListNoteSerializer
        return super().list(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    queryset = b4_models.User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.get_model_serializer_class(
        b4_models.User,
        local_exclude=[]
    )

    @action(methods=['get'], detail=False)
    def current_user(self, request, *args, **kwargs):
        self.serializer_class = serializers.get_model_serializer_class(
            b4_models.User,
            local_fields=['username', 'id']
        )
        obj = b4_models.User.objects.get(id=request.user.id)
        ser_obj = self.serializer_class(obj)
        return Response(ser_obj.data)

    @action(methods=['get'], detail=False)
    def get_for_plan(self, request, *args, **kwargs):
        self.serializer_class = serializers.get_model_serializer_class(
            b4_models.User,
            local_fields=['username', 'id']
        )
        qs = self.queryset
        if not request.user.is_superuser:
            qs = b4_models.User.objects.filter(id=request.user.id)
        ser_qs = self.serializer_class(qs, many=True)
        return Response(ser_qs.data)


@api_view(['GET'])
def get_section_list_view(request):
    qs = b4_models.Section.objects.filter(is_active=True)
    ser_class = serializers.get_model_serializer_class(
        b4_models.Section,
        local_fields=['id', 'name']
    )
    ser = ser_class(qs, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)
