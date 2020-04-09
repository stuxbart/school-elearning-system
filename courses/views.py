from django.shortcuts import render
from django.views.generic import ListView

from .models import Subject
# Create your views here.
class CourseListView(ListView):
    model = Subject
    template_name = 'courses/course_list.html'    

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        request = self.request
        if request.user.is_authenticated:
            context['my_courses'] = request.user.courses.all()
        return context