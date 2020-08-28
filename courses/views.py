from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Course, Text, Image, File, Video, Membership, Category
from activity.mixins import CourseViewedMixin


class CourseListView(ListView):
    queryset = Course.objects.all()
    template_name = 'courses/course_list.html'

    def get_queryset(self):
        return Course.objects.exclude(participants__id=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        request = self.request
        if request.user.is_authenticated:
            context['my_courses'] = request.user.courses.all()
        return context


class CategoryCoursesListView(DetailView):
    queryset = Category.objects.all()
    template_name = 'courses/course_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = self.object.course_set.all()
        return context


class CourseDetailView(CourseViewedMixin, DetailView):
    queryset = Course.objects.all()
    template_name = 'courses/course_details.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Course, slug=slug)
        return instance


def enroll_course(request):
    course_id = request.POST.get('course_id')
    course_obj = get_object_or_404(Course, id=course_id)
    course_access_key = request.POST.get('course_access_key')
    # Add course_access_key verification
    if course_obj.access_key == course_access_key:
        user = request.user
        if user.is_authenticated:
            # user.courses.add(course_id, method="key")
            m = Membership(
                user=request.user,
                course=course_obj,
                method="key"
            )
            m.save()
            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'log in'}, status=400)
    return JsonResponse({'message': 'error'}, status=400)


class TextDetailView(DetailView):
    model = Text
    template_name = 'courses/content/text.html'


class ImageDetailView(DetailView):
    model = Image
    template_name = 'courses/content/image.html'


class FileDetailView(DetailView):
    model = File
    template_name = 'courses/content/file.html'


class VideoDetailView(DetailView):
    model = Video
    template_name = 'courses/content/video.html'
