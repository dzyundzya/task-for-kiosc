from django.urls import path, include
from rest_framework.routers import DefaultRouter

from server.apps.workers.views import WorkerImportView, WorkerViewSet

router = DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='workers')


urlpatterns = [
    path('workers/import/', WorkerImportView.as_view(), name='worker-import'),
    path('', include(router.urls)),
]
