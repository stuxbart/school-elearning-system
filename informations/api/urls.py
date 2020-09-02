from django.urls import path, include
from rest_framework import routers

from .views import NewsViewSet

router = routers.DefaultRouter()
router.register('', NewsViewSet, 'news')

urlpatterns = [
    path('', include(router.urls))
]
