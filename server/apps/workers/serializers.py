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
            'email', 'hired_date', 'created_at', 'updated_at'
        )


