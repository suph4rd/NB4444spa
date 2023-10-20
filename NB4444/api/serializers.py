from django.contrib.auth import get_user_model
from rest_framework import serializers

from B4 import models as b4_models


def get_model_serializer_class(
        local_models,
        local_exclude: None | list = None,
        local_fields: str | list = "__all__",
        local_depth: int = 0
):
    """
    This method made for you typical ModelSerializer class.
    If you write param local_exclude, you don't need write param local_fields,
    because this param won't used.

    :param local_models: instance of models.Model
    :param local_fields: fields of model
    :param local_exclude: fields of model, which you want exclude
    :param local_depth: depth of serializer class
    :return: ModelSerializer
    """

    class CustomModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = local_models
            if local_exclude:
                exclude = local_exclude
            else:
                fields = local_fields
            depth = local_depth
    return CustomModelSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'is_superuser']


class ListPlanSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    created_at = serializers.DateTimeField(format="%d %B %Y")

    class Meta:
        model = b4_models.Plan
        fields = ['id', 'name', 'user', 'created_at']


class ListNoteSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    created_at = serializers.DateTimeField(format="%d %B %Y")

    class Meta:
        model = b4_models.Note
        fields = ['id', 'text', 'image', 'user', 'created_at']


class ListTaskSerializer(serializers.ModelSerializer):
    plan = get_model_serializer_class(
        b4_models.Plan,
        local_fields=['id', 'name']
    )()
    section = get_model_serializer_class(
        b4_models.Section,
        local_fields=['id', 'name']
    )()
    created_at = serializers.DateTimeField(format="%d %B %Y")

    class Meta:
        model = b4_models.Task
        fields = ['id', 'plan', 'section', 'description', 'is_ready', 'created_at']


class DetailPlanSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    created_at = serializers.DateTimeField(format="%d %B %Y")
    task_set = ListTaskSerializer(many=True)

    class Meta:
        model = b4_models.Plan
        fields = ['id', 'name', 'user', 'created_at', 'task_set']
