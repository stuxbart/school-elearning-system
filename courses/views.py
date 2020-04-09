from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

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

class CourseDetailView(DetailView):
    queryset = Subject.objects.all()
    template_name = 'courses/course_details.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Subject, slug=slug)
        return instance