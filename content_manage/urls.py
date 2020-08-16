from django.urls import path, include

from .views import (
        ManageCourseList,
        ManageCourseEdit,
        CourseAddContentView,
        CreateTextContentView,
        CreateImageContentView,
        CreateFileContentView,
        CreateVideoContentView,
        CreateModuleContentView,
        ManageCourseMainView,
        EditModuleContentView,
        DeleteModuleView,
        DeleteCourseView,
        ManageCourseParticipantsView,
        DeleteContentView,
        ShowHideContentView,
        ShowModuleView,
        ContentOrderView
    )

app_name = 'manage'

urlpatterns = [
    path('', ManageCourseList.as_view(), name='list'),
    path('course/', ManageCourseEdit.as_view(), name="create"),
    path('course/<slug>/edit', ManageCourseEdit.as_view(), name="update"),
    path('course/<slug>/delete', DeleteCourseView.as_view(), name="delete"),

    path('course/<slug>', ManageCourseMainView.as_view(), name="course_home"),
    path('course/<slug>/add', CourseAddContentView.as_view(), name="add_content"),
    path('course/<slug>/participants', ManageCourseParticipantsView.as_view(), name="participants"),


    path('course/<slug>/add-module', CreateModuleContentView.as_view(), name="add_module"),
    path('course/show-module/<pk>/', ShowModuleView.as_view(), name="show_module"),
    path('course/edit-module/<pk>/', EditModuleContentView.as_view(), name="edit_module"),
    path('course/delete-module/<pk>/', DeleteModuleView.as_view(), name="delete_module"),

    path('course/add/text', CreateTextContentView.as_view(), name='add_content_text'),
    path('course/add/image', CreateImageContentView.as_view(), name='add_content_image'),
    path('course/add/file', CreateFileContentView.as_view(), name='add_content_file'),
    path('course/add/video', CreateVideoContentView.as_view(), name='add_content_video'),

    path('course/edit/text/<pk>/', CreateTextContentView.as_view(), name='edit_content_text'),
    path('course/edit/image/<pk>/', CreateImageContentView.as_view(), name='edit_content_image'),
    path('course/edit/file/<pk>/', CreateFileContentView.as_view(), name='edit_content_file'),
    path('course/edit/video/<pk>/', CreateVideoContentView.as_view(), name='edit_content_video'),

    path('course/move-content/', ContentOrderView.as_view(), name='move_content'),
    path('course/delete-content/<pk>/', DeleteContentView.as_view(), name='delete_content'),
    path('course/show-hide-content/<pk>/', ShowHideContentView.as_view(), name='show_hide_content')
]
