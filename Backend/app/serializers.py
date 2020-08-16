from rest_framework import serializers
from .models import OperationManager, Mobilizer, Students, Event, CustomToken


class OperationManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationManager
        fields = "__all__"


class MobilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobilizer
        fields = "__all__"


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class CustomTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomToken
        fields = "__all__"
