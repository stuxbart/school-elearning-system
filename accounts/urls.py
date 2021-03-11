from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from .views import (
    login_view, 
    logout_view, 
    UserHomeView, 
    UserDetailView, 
    UserSearchListView,
    UserEditView,
    UserPhotoUpdate,
    UserPasswordChangeView,
    UserInfoUpdate
)

app_name = 'accounts'

urlpatterns = [
    path('search/', UserSearchListView.as_view(), name="search"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserHomeView.as_view(), name='my_profile'),
    path('profile/edit', UserEditView.as_view(), name="my_profile_update"),
    path('profile/edit/photo', UserPhotoUpdate.as_view(), name="my_profile_update_photo"),
    path('profile/edit/info', UserInfoUpdate.as_view(), name="my_profile_update_info"),
    path('profile/change-password/', UserPasswordChangeView.as_view(), name="password_change"),
    path('user/<pk>/', UserDetailView.as_view(), name="user_detail"),
]
