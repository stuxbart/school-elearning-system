from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers
from .views import (
    CategoryViewSet,
    CourseListCreateAPIView,
    CourseDetail
)

router = routers.DefaultRouter()
router.register('category', CategoryViewSet, basename="category")

urlpatterns = [
    path('', CourseListCreateAPIView.as_view()),
    path('<slug>/', CourseDetail.as_view(), name="course-detail"),
    path('', include(router.urls)),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
