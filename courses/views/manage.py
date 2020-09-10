from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import ListView, FormView, DetailView, View, DeleteView, CreateView, UpdateView
from django.http import JsonResponse
from operator import itemgetter
import json
from ..forms import (
    TextContentForm,
    ImageContentForm,
    FileContentForm,
    VideoContentForm,
    ModuleCreateForm,
    AddUserToCourseForm,
    CourseCreateForm
)

from ..mixins import IsTeacherMixin
from ..models import Course, Content, Module, Membership

from activity.models import CourseViewed


class ManageCourseList(LoginRequiredMixin, IsTeacherMixin, ListView):
    model = Course
    template_name = 'courses/list.html'

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class CourseCreateView(LoginRequiredMixin, IsTeacherMixin, CreateView):
    form_class = CourseCreateForm
    template_name = 'courses/edit.html'

    def get_success_url(self):
        return reverse('courses:manage_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseEditView(LoginRequiredMixin, IsTeacherMixin, UpdateView):
    form_class = CourseCreateForm
    template_name = 'courses/edit.html'

    def get_success_url(self):
        return reverse('courses:manage_list')

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class DeleteCourseView(LoginRequiredMixin, IsTeacherMixin, DeleteView):
    model = Course
    template_name = 'courses/delete.html'

    def get_success_url(self):
        return reverse('courses:manage_list')

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class CourseAddContentView(LoginRequiredMixin, IsTeacherMixin, DetailView):
    model = Course
    template_name = 'courses/add_content.html'

    def get_context_data(self, **kwargs):
        context = super(CourseAddContentView, self).get_context_data(**kwargs)
        context["forms"] = {
            'text': {'instance': TextContentForm(), 'action': reverse('courses:add_content_text')},
            'image': {'instance': ImageContentForm(), 'action': reverse('courses:add_content_image')},
            'file': {'instance': FileContentForm(), 'action': reverse('courses:add_content_file')},
            'video': {'instance': VideoContentForm(), 'action': reverse('courses:add_content_video')},
            'module': {'instance': ModuleCreateForm(),
                       'action': reverse('courses:add_module', kwargs={'slug': context['object'].slug})}
        }
        return context


class CreateTextContentView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = TextContentForm
    success_url = '/'

    def form_valid(self, form):
        pk = form.cleaned_data.get('content_id') or None
        if pk is not None:
            content = Content.objects.get(pk=pk)
            visible = form.cleaned_data.get('visible')
            content.item.title = form.cleaned_data.get('title')
            content.visible = form.cleaned_data.get('visible')
            content.item.content = form.cleaned_data.get('content')

            content.item.save()
            content.save()

            if self.request.is_ajax():
                data = {
                    'message': 'success',
                }
                return JsonResponse(data)
            else:
                return response
        else:
            response = super().form_valid(form)
            module_id = form.cleaned_data.get('module_id')
            visible = form.cleaned_data.get('visible')
            module_obj = get_object_or_404(Module, pk=module_id)
            form.instance.owner = self.request.user
            item = form.save()
            content_obj = Content(module=module_obj, item=item, visible=visible)
            content_obj.save()
            if self.request.is_ajax():
                data = {
                    'message': 'success',
                }
                return JsonResponse(data)
            else:
                return response

    def form_invalid(self, form):
        print(form.errors)


class CreateImageContentView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = ImageContentForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
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
                'message': 'error',
            }
            return JsonResponse(data, status=400)
        else:
            return response


class CreateFileContentView(LoginRequiredMixin, IsTeacherMixin, FormView):
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
                'message': 'error',
            }
            return JsonResponse(data, status=400)
        else:
            return response


class CreateVideoContentView(LoginRequiredMixin, IsTeacherMixin, FormView):
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


class CreateModuleContentView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = ModuleCreateForm
    success_url = '/'
    template_name = 'courses/success.html'

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


class EditModuleContentView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = ModuleCreateForm
    success_url = '/'
    template_name = 'courses/success.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print(self.kwargs.get('pk'))
        if form.is_valid():
            # slug = kwargs.get('slug')
            # course_obj = get_object_or_404(Course, slug=slug)
            # form.instance.course = course_obj
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        module_id = self.kwargs.get('pk', None)
        if module_id is None:
            if self.request.is_ajax():
                data = {
                    'message': 'error',
                }
                return JsonResponse(data)
            else:
                return response
        module_obj = get_object_or_404(Module, id=module_id)
        if self.request.user != module_obj.course.owner:
            if self.request.is_ajax():
                data = {
                    'message': 'error',
                }
                return JsonResponse(data)
            else:
                return response
        cd = form.cleaned_data

        module_obj.title = cd['title']
        module_obj.description = cd['description']
        module_obj.save()
        if self.request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response


class DeleteModuleView(LoginRequiredMixin, IsTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        module_id = self.kwargs.get('pk', None)
        request = self.request
        if module_id is not None:
            module_obj = get_object_or_404(Module, id=module_id)
            if request.user == module_obj.course.owner:
                module_obj.delete()
                if request.is_ajax():
                    data = {
                        'message': 'Deleted',
                    }
                    return JsonResponse(data)
                else:
                    return response
        if request.is_ajax():
            data = {
                'message': 'Error',
            }
            return JsonResponse(data)
        else:
            return response


class ShowModuleView(LoginRequiredMixin, IsTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        module_id = self.kwargs.get('pk', None)
        request = self.request
        if module_id is not None:
            module_obj = get_object_or_404(Module, id=module_id)
            module_obj.visible = not module_obj.visible

            module_obj.save()
            if request.is_ajax():
                data = {
                    'message': 'success',
                }
                return JsonResponse(data)
            else:
                return response
        if request.is_ajax():
            data = {
                'message': 'Error',
            }
            return JsonResponse(data)
        else:
            return response


class ManageCourseMainView(LoginRequiredMixin, IsTeacherMixin, DetailView):
    model = Course
    template_name = 'courses/course_main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ManageCourseMainView, self).get_context_data(*args, **kwargs)
        obj = context['object']
        participants = obj.participants.all()
        last_activities = []
        never_active = []
        for p in participants:
            activities = CourseViewed.objects.filter(user=p, course=obj)
            if activities.exists():
                last = activities.first()
                last_activities.append({'user': p, 'last': last.timestamp})
            else:
                never_active.append({'user': p, 'last': None})
        context['last_activities'] = sorted(last_activities, key=itemgetter('last'), reverse=True)
        context['last_activities'] += never_active
        return context


class ManageCourseParticipantsView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = AddUserToCourseForm
    template_name = 'courses/course_participants.html'

    # success_url = reverse("courses:participants", kwargs={"slug": })

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        context['participants'] = Membership.objects.filter(course=course)
        return context

    def get_success_url(self):
        return reverse("courses:participants", kwargs={'slug': self.kwargs['slug']})

    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
    # return render(request, self.template_name, self.get_context_data())

    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        course.participants.set(form.cleaned_data['participants'], through_defaults={'method': 'owner'})
        course.save()
        return super().form_valid(form)


class DeleteContentView(LoginRequiredMixin, IsTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        content = Content.objects.get(pk=self.kwargs['pk'])
        content.delete()
        if request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)


class ShowHideContentView(LoginRequiredMixin, IsTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        content = Content.objects.get(pk=self.kwargs['pk'])
        content.visible = not content.visible
        content.save()
        if request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response


class ContentOrderView(LoginRequiredMixin, IsTeacherMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        pk = json_data.get('id')
        up_down = json_data.get('direction')

        content = Content.objects.get(pk=pk)
        module = content.module
        if up_down == "up":
            if content.order == 1:
                if request.is_ajax():
                    data = {
                        'message': 'success',
                    }
                    return JsonResponse(data)
                else:
                    return response
            else:
                up_content = module.content_set.get(order=content.order - 1)

                up_content.order = content.order
                content.order -= 1
                content.save()
                up_content.save()

                if request.is_ajax():
                    data = {
                        'message': 'success',
                    }
                    return JsonResponse(data)
                else:
                    return response
        elif up_down == "down":
            if content.order == module.content_set.latest('order').order:
                if request.is_ajax():
                    data = {
                        'message': 'success',
                    }
                    return JsonResponse(data)
                else:
                    return response
            else:
                down_content = module.content_set.get(order=content.order + 1)

                down_content.order = content.order
                content.order += 1
                content.save()
                down_content.save()

                if request.is_ajax():
                    data = {
                        'message': 'success',
                    }
                    return JsonResponse(data)
                else:
                    return response

# class ModuleOrderView(LoginRequiredMixin, IsTeacherMixin, View):
#     def post(self, request, *args, **kwargs):
#         data = request.body.decode('utf-8')
#         json_data = json.loads(data)

#         pk = json_data.get('id')
#         up_down = json_data.get('direction')

#         content = Content.objects.get(pk=pk)
#         module = content.module
#         if up_down == "up":
#             if content.order == 1:
#                 if request.is_ajax():
#                     data = {
#                         'message': 'success',
#                     }
#                     return JsonResponse(data)
#                 else:
#                     return response
#             else:
#                 up_content = module.content_set.get(order=content.order-1)

#                 up_content.order = content.order
#                 content.order -= 1
#                 content.save()
#                 up_content.save()

#                 if request.is_ajax():
#                     data = {
#                         'message': 'success',
#                     }
#                     return JsonResponse(data)
#                 else:
#                     return response
#         elif up_down == "down":
#             if content.order == module.content_set.latest('order').order:
#                 if request.is_ajax():
#                     data = {
#                         'message': 'success',
#                     }
#                     return JsonResponse(data)
#                 else:
#                     return response
#             else:
#                 down_content = module.content_set.get(order=content.order+1)

#                 down_content.order = content.order
#                 content.order += 1
#                 content.save()
#                 down_content.save()

#                 if request.is_ajax():
#                     data = {
#                         'message': 'success',
#                     }
#                     return JsonResponse(data)
#                 else:
#                     return response
