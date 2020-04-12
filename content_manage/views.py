from django.shortcuts import render
from django.views.generic import ListView

from courses.models import Course

class ManageCourseList(ListView):
    model = Course
    template_name='content_manage/list.html'