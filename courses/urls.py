from django.urls import path

from .views import (
    CourseListView,
    CourseDetailView,
    enroll_course,
    TextDetailView,
    ImageDetailView,
    FileDetailView,
    VideoDetailView,
    CategoryCoursesListView
)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='home'),
    path('category/<slug>/', CategoryCoursesListView.as_view(), name="category"),
    path('details/<slug>/', CourseDetailView.as_view(), name='details'),
    path('enroll/', enroll_course, name='enroll'),
    path('details/content/text/<pk>', TextDetailView.as_view(), name='text_detail'),
    path('details/content/image/<pk>', ImageDetailView.as_view(), name='image_detail'),
    path('details/content/file/<pk>', FileDetailView.as_view(), name='file_detail'),
    path('details/content/video/<pk>', VideoDetailView.as_view(), name='video_detail'),
]
