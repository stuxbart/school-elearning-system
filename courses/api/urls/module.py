from django.urls import include, path

from rest_framework import routers

from ..views import (
    ModuleViewSet
)

router = routers.DefaultRouter()
router.register('', ModuleViewSet, basename="module")

urlpatterns = [
    path('', include(router.urls)),
]
