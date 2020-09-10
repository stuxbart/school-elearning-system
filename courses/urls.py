from django.urls import path, include

from .views import (
    CourseListView,
    CourseDetailView,
    enroll_course,
    TextDetailView,
    ImageDetailView,
    FileDetailView,
    VideoDetailView,
    CategoryCoursesListView,
    ManageCourseList,
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
    ContentOrderView,
    CourseCreateView,
    CourseEditView
)

app_name = 'courses'

manage_urls = [
    path('', ManageCourseList.as_view(), name='manage_list'),
    path('course/', CourseCreateView.as_view(), name="create"),
    path('course/<slug>/edit', CourseEditView.as_view(), name="update"),
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

urlpatterns = [
    path('', CourseListView.as_view(), name='home'),
    path('category/<slug>/', CategoryCoursesListView.as_view(), name="category"),
    path('details/<slug>/', CourseDetailView.as_view(), name='details'),
    path('enroll/', enroll_course, name='enroll'),
    path('details/content/text/<pk>', TextDetailView.as_view(), name='text_detail'),
    path('details/content/image/<pk>', ImageDetailView.as_view(), name='image_detail'),
    path('details/content/file/<pk>', FileDetailView.as_view(), name='file_detail'),
    path('details/content/video/<pk>', VideoDetailView.as_view(), name='video_detail'),

    path('manage/', include(manage_urls))
]
