from django.urls import include, path

from rest_framework import routers

from ..views import (
    TextContentViewSet,
    ImageContentViewSet,
    VideoContentViewSet,
    FileContentViewSet
)

router = routers.DefaultRouter()
router.register('text', TextContentViewSet, basename="text")
router.register('image', ImageContentViewSet, basename="image")
router.register('video', VideoContentViewSet, basename="video")
router.register('file', FileContentViewSet, basename="file")

urlpatterns = [
    path('', include(router.urls)),
]
