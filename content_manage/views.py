from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, FormView, DetailView
from django.http import JsonResponse

from .forms import (
        CourseUpdateForm,
        TextContentForm, 
        ImageContentForm, 
        FileContentForm, 
        VideoContentForm, 
        ModuleCreateForm
    )
from courses.models import Course, Content, Module, Text, Image, File

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

class CourseAddContentView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'content_manage/add_content.html'

    def get_context_data(self, **kwargs):
        context = super(CourseAddContentView, self).get_context_data(**kwargs)
        context["forms"] = {
                'text': {'instance' :TextContentForm(),'action': reverse('manage:add_content_text')},
                'image': {'instance' :ImageContentForm(), 'action': reverse('manage:add_content_image')},
                'file': {'instance': FileContentForm(), 'action': reverse('manage:add_content_file')},
                'video': {'instance': VideoContentForm(), 'action': reverse('manage:add_content_video')},
                'module': {'instance': ModuleCreateForm(), 'action': reverse('manage:add_module', kwargs={'slug': context['object'].slug})}
            }
        return context
    

class CreateTextContentView(LoginRequiredMixin, FormView):
    form_class = TextContentForm
    success_url = '/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        module_id = form.cleaned_data.get('module_id')
        module_obj = get_object_or_404(Module, pk=module_id)
        form.instance.owner = self.request.user
        item = form.save()
        content_obj = Content(module=module_obj, item=item)
        content_obj.save()
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response

class CreateImageContentView(LoginRequiredMixin, FormView):
    form_class = ImageContentForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print('files: ', request.FILES)
        print('post: ', request.POST)
        print(form.errors)
        
        if form.is_valid():
            # for f in files:
            #     ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        module_id = form.cleaned_data.get('module_id')
        module_obj = get_object_or_404(Module, pk=module_id)
        form.instance.owner = self.request.user
        item = form.save()
        content_obj = Content(module=module_obj, item=item)
        content_obj.save()
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data, status=400)
        else:
            return response


class CreateFileContentView(LoginRequiredMixin, FormView):
    form_class = FileContentForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        module_id = form.cleaned_data.get('module_id')
        module_obj = get_object_or_404(Module, pk=module_id)
        form.instance.owner = self.request.user
        item = form.save()
        content_obj = Content(module=module_obj, item=item)
        content_obj.save()
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'not gut',
            }
            return JsonResponse(data, status=400)
        else:
            return response


class CreateVideoContentView(LoginRequiredMixin, FormView):
    form_class = VideoContentForm
    success_url = '/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        module_id = form.cleaned_data.get('module_id')
        module_obj = get_object_or_404(Module, pk=module_id)
        form.instance.owner = self.request.user
        item = form.save()
        content_obj = Content(module=module_obj, item=item)
        content_obj.save()
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data, status=400)
        else:
            return response


class CreateModuleContentView(LoginRequiredMixin, FormView):
    form_class = ModuleCreateForm
    success_url = '/'
    template_name = 'content_manage/success.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            slug = kwargs.get('slug')
            course_obj = get_object_or_404(Course, slug=slug)
            form.instance.course = course_obj
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response

class ManageCourseMainView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'content_manage/course_main.html'

    