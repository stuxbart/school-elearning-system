
from django.urls import path, include

from .views import CourseListView, CourseDetailView

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='home'),
    path('details/<slug>/', CourseDetailView.as_view(), name='details'),    
]
