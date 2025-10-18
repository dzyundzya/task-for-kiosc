from typing import Any

from django.db import IntegrityError
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import validate_email
from rest_framework import serializers

from server.apps.workers.models import Worker
from server.apps.users.serializers import UserSerializer


class WorkerListSerializer(serializers.ModelSerializer[Worker]):  # type: ignore[misc]
    class Meta:
        model = Worker
        fields = (
            'id', 
            'first_name', 
            'middle_name', 
            'last_name', 
            'position', 
            'is_active'
        )


class WorkerDetailSerializer(WorkerListSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta(WorkerListSerializer.Meta):
        fields = WorkerListSerializer.Meta.fields + (  # type: ignore[assignment]
            'created_by', 'email', 'hired_date', 'created_at', 'updated_at'
        )


class WorkerCreateUpdateSerializer(WorkerListSerializer):
    email = serializers.EmailField()

    class Meta(WorkerListSerializer.Meta):
        fields = WorkerListSerializer.Meta.fields + ('email',)  # type: ignore[assignment]
        read_only_fields = ('id',)

    def validate_email(self, data: str | None) -> str | None:
        validate_email(data)
        return data

    def create(self, validated_data: dict[str, Any]) -> Any:
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            raise serializers.ValidationError(
                {'email': 'The email already exists.'}
            )


class WorkerImportSerializer(serializers.Serializer):  # type: ignore[misc]
    xl_file = serializers.FileField()

    def validate_xl_file(self, value: UploadedFile) -> UploadedFile:
        """Validate that uploaded file is Excel (.xlsx)."""
        if not value.name or not value.name.endswith('.xlsx'):
            raise serializers.ValidationError(
                'Файл должен быть в формате .xlsx',
            )
        return value
