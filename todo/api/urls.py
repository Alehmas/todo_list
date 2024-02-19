from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
