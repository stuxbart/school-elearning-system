from django.urls import path, include

from .views import (
        ManageCourseList,
        ManageCourseEdit,
        CourseAddContentView,
        CreateTextContentView,
        CreateImageContentView,
        CreateFileContentView,
        CreateVideoContentView,
        CreateModuleContentView
    )

app_name = 'manage'

urlpatterns = [
    path('', ManageCourseList.as_view(), name='list'),
    path('course/', ManageCourseEdit.as_view(), name="create"),
    path('course/<slug>/edit', ManageCourseEdit.as_view(), name="update"),
    path('course/<slug>/add', CourseAddContentView.as_view(), name="add_content"),
    path('course/<slug>/add-module', CreateModuleContentView.as_view(), name="add_module"),
    path('course/add/text', CreateTextContentView.as_view(), name='add_content_text'),
    path('course/add/image', CreateImageContentView.as_view(), name='add_content_image'),
    path('course/add/file', CreateFileContentView.as_view(), name='add_content_file'),
    path('course/add/video', CreateVideoContentView.as_view(), name='add_content_video'),
]
