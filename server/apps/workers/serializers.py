from typing import Any

from django.core.files.uploadedfile import UploadedFile
from django.core.validators import validate_email
from django.db import IntegrityError
from rest_framework import serializers

from server.apps.users.serializers import UserSerializer
from server.apps.workers.models import Worker


class WorkerListSerializer(serializers.ModelSerializer[Worker]):  # type: ignore[misc]
    """Serializer for listing workers."""

    class Meta:
        model = Worker
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'position',
            'is_active',
        )


class WorkerDetailSerializer(WorkerListSerializer):
    """Serializer for detailed worker information."""

    created_by = UserSerializer(read_only=True)

    class Meta(WorkerListSerializer.Meta):
        fields = (
            *WorkerListSerializer.Meta.fields,  # type: ignore[assignment]
            'created_by',
            'email',
            'hired_date',
            'created_at',
            'updated_at',
        )


class WorkerCreateUpdateSerializer(WorkerListSerializer):
    """Serializer for creating and updating workers."""

    email = serializers.EmailField()

    class Meta(WorkerListSerializer.Meta):
        fields = (*WorkerListSerializer.Meta.fields, 'email')  # type: ignore[assignment]
        read_only_fields = ('id',)

    def validate_email(self, email: str | None) -> str | None:
        """Validate that the provided email address is valid."""
        validate_email(email)
        return email

    def create(self, validated_data: dict[str, Any]) -> Any:
        """Create a new worker instance and handle email uniqueness."""
        try:
            return super().create(validated_data)
        except IntegrityError as err:
            raise serializers.ValidationError({
                'email': 'The email already exists.'
            }) from err


class WorkerImportSerializer(serializers.Serializer):  # type: ignore[misc]
    """Serializer for validating worker import Excel file."""

    xl_file = serializers.FileField()

    def validate_xl_file(self, uploaded_file: UploadedFile) -> UploadedFile:
        """Validate that uploaded file is Excel (.xlsx)."""
        if not uploaded_file.name or not uploaded_file.name.endswith('.xlsx'):
            raise serializers.ValidationError(
                'File must be in the format .xlsx',
            )
        return uploaded_file
