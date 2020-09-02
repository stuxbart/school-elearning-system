from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers
from .views import (
    CategoryViewSet,
    CourseListCreateAPIView,
    CourseDetail,
    CourseEnrolAPIView
)

router = routers.DefaultRouter()
router.register('category', CategoryViewSet, basename="category")

urlpatterns = [
    path('', CourseListCreateAPIView.as_view()),
    path('<slug>/', CourseDetail.as_view(), name="course-detail"),
    path('<slug>/enroll', CourseEnrolAPIView.as_view(), name="course-enroll"),
    path('', include(router.urls)),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
