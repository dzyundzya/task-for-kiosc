from rest_framework.routers import DefaultRouter

from server.apps.workers.views import WorkerViewSet

router = DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='workers')


urlpatterns = router.urls
