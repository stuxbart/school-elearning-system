from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers
from .views import (
    CategoryViewSet,
    CourseListCreateAPIView,
    CourseDetail,
    CourseEnrolAPIView,
    # ModuleListCreateAPIView,
    # ModuleRetrieveUpdateDestroyAPIView
    ModuleViewSet
)

router = routers.DefaultRouter()
router.register('category', CategoryViewSet, basename="category")
router.register('module', ModuleViewSet, basename="module")

urlpatterns = [
    path('', include(router.urls)),
    path('', CourseListCreateAPIView.as_view()),
    path('<slug>/', CourseDetail.as_view(), name="course-detail"),
    path('<slug>/enroll', CourseEnrolAPIView.as_view(), name="course-enroll"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
