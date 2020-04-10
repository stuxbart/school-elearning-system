from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
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

def enroll_course(request):
    print(request.POST)
    course_id = request.POST.get('course_id')
    course_obj = get_object_or_404(Subject, id=course_id)
    course_access_key = request.POST.get('course_access_key')
    # Add course_access_key verification
    if course_obj.access_key == course_access_key:
        user = request.user
        if user.is_authenticated:
            user.courses.add(course_id)
            return JsonResponse({'message': 'gut'}, status=200)
        else:
            return JsonResponse({'message': 'zaloguj sie'}, status=400)
    return JsonResponse({'message': 'not gut'}, status=400)