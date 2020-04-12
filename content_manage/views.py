from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, FormView

from .forms import CourseUpdateForm
from courses.models import Course

class ManageCourseList(LoginRequiredMixin, ListView):
    model = Course
    template_name='content_manage/list.html'

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

class ManageCourseEdit(LoginRequiredMixin, FormView):
    form_class = CourseUpdateForm
    template_name = 'content_manage/edit.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ManageCourseEdit, self).get_context_data(*args, **kwargs)
        print(args, kwargs)
        if self.object:
            context['object'] = self.object
        return context

    def get(self, request, *args, **kwargs):
        if kwargs.get('slug', None):
            slug = kwargs.get('slug')
            self.object = get_object_or_404(Course, slug=slug)
            self.initial = {
                    'title': self.object.title,
                    'overview': self.object.overview,
                    'access_key': self.object.access_key
                }
        else:
            self.object = None
        return super(ManageCourseEdit, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if kwargs.get('slug', None):
            slug = kwargs.get('slug')
            self.object = get_object_or_404(Course, slug=slug)
            self.success_url = reverse('manage:update',kwargs={'slug': slug})
        else:
            self.object = Course(owner=request.user)
        return super(ManageCourseEdit, self).post(request, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        self.object.title = form.cleaned_data.get('title')
        self.object.overview = form.cleaned_data.get('overview')
        self.object.access_key = form.cleaned_data.get('access_key')
        self.object.save()
        self.success_url = reverse('manage:update',kwargs={'slug': self.object.slug})
        return super(ManageCourseEdit, self).form_valid(form)

