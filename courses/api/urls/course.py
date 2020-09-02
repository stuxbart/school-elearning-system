from django.urls import path
from ..views import (
    CourseListCreateAPIView,
    CourseDetail,
    CourseEnrolAPIView,
)

urlpatterns = [
    path('', CourseListCreateAPIView.as_view()),
    path('<slug>/', CourseDetail.as_view(), name="course-detail"),
    path('<slug>/enroll', CourseEnrolAPIView.as_view(), name="course-enroll"),
]

