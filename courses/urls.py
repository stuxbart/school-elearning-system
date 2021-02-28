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
    ModuleCreateView,
    CourseManageDetailView,
    ModuleUpdateView,
    ModuleDeleteView,
    DeleteCourseView,
    CourseParticipantsManageDetailView,
    CourseAdminsManageDetailView,
    CourseAdminUpdateView,
    CourseAdminDeleteView,
    ContentDeleteView,
    ContentShowHideView,
    ModuleShowHideView,
    ContentOrderView,
    CourseCreateView,
    CourseEditView,
    ModuleOrderView,
    TextContentCreateView,
    TextContentUpdateView,
    ImageContentCreateView,
    ImageContentUpdateView,
    FileContentCreateView,
    FileContentUpdateView,
    VideoContentCreateView,
    VideoContentUpdateView
)

app_name = 'courses'

manage_urls = [
    path('', ManageCourseList.as_view(), name='manage_list'),
    path('course/', CourseCreateView.as_view(), name="create"),
    path('course/<slug>/edit', CourseEditView.as_view(), name="update"),
    path('course/<slug>/delete', DeleteCourseView.as_view(), name="delete"),

    path('course/<slug>', CourseManageDetailView.as_view(), name="course_home"),
    path('course/<slug>/add', CourseAddContentView.as_view(), name="add_content"),
    path('course/<slug>/participants', CourseParticipantsManageDetailView.as_view(), name="participants"),
    path('course/<slug>/admins', CourseAdminsManageDetailView.as_view(), name="admins"),
    path('course/<slug>/admins/<pk>/delete', CourseAdminDeleteView.as_view(), name="delete_admins"),
    path('course/<slug>/admins/<pk>/update', CourseAdminUpdateView.as_view(), name="update_course_admin"),

    path('course/<slug>/add-module', ModuleCreateView.as_view(), name="add_module"),
    path('course/show-module/<pk>/', ModuleShowHideView.as_view(), name="show_module"),
    path('course/move-module/', ModuleOrderView.as_view(), name='move_module'),
    path('course/edit-module/<pk>/', ModuleUpdateView.as_view(), name="edit_module"),
    path('course/delete-module/<pk>/', ModuleDeleteView.as_view(), name="delete_module"),

    path('course/create/text', TextContentCreateView.as_view(), name='create_text_ajax'),
    path('course/<pk>/create/text', TextContentCreateView.as_view(), name='create_text'),
    path('course/update/text', TextContentUpdateView.as_view(), name='update_text_ajax'),
    path('course/update/text/<pk>', TextContentUpdateView.as_view(), name='update_text'),

    path('course/create/image', ImageContentCreateView.as_view(), name='create_image_ajax'),
    path('course/<pk>/create/image', ImageContentCreateView.as_view(), name='create_image'),
    path('course/update/image', ImageContentUpdateView.as_view(), name='update_image_ajax'),
    path('course/update/image/<pk>', ImageContentUpdateView.as_view(), name='update_image'),

    path('course/create/file', FileContentCreateView.as_view(), name='create_file_ajax'),
    path('course/<pk>/create/file', FileContentCreateView.as_view(), name='create_file'),
    path('course/update/file', FileContentUpdateView.as_view(), name='update_file_ajax'),
    path('course/update/file/<pk>', FileContentUpdateView.as_view(), name='update_file'),

    path('course/create/video', VideoContentCreateView.as_view(), name='create_video_ajax'),
    path('course/<pk>/create/video', VideoContentCreateView.as_view(), name='create_video'),
    path('course/update/video', VideoContentUpdateView.as_view(), name='update_video_ajax'),
    path('course/update/video/<pk>', VideoContentUpdateView.as_view(), name='update_video'),

    path('course/move-content/', ContentOrderView.as_view(), name='move_content'),
    path('course/delete-content/<pk>/', ContentDeleteView.as_view(), name='delete_content'),
    path('course/show-hide-content/<pk>/', ContentShowHideView.as_view(), name='show_hide_content')
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
