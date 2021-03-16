from django.urls import path

from .views import (
    StudentRecordBookDetailView,
    TeacherRecordBookListView,
    TeacherRecordBookDetailView,
    GradeCreateView,
    GradeUpdateView,
    GradeDeleteView,
    GradeDetailView
)

app_name = "gradebook"

urlpatterns = [
    path("my-grades", StudentRecordBookDetailView.as_view(), name="user_home"),
    path("my-grades/<pk>", StudentRecordBookDetailView.as_view(), name="user_home"),
    path("gradebooks/", TeacherRecordBookListView.as_view(), name="teacher_home"),
    path("gradebooks/<pk>", TeacherRecordBookDetailView.as_view(), name="teacher_gradebook_detail"),
    path('gradebook/<pk>/add-grade', GradeCreateView.as_view(), name="create_grade"),
    path('gradebook/detail-grade/<pk>', GradeDetailView.as_view(), name="detail_grade"),
    path('gradebook/update-grade/<pk>', GradeUpdateView.as_view(), name="update_grade"),
    path('gradebook/delete-grade/<pk>', GradeDeleteView.as_view(), name="delete_grade"),
]