from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import ListView, FormView, DetailView, View, DeleteView, CreateView, UpdateView
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Subquery, OuterRef
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
            'text': {
                'instance': TextContentForm(),
                'action': reverse('courses:add_content_text')
            },
            'image': {
                'instance': ImageContentForm(),
                'action': reverse('courses:add_content_image')
            },
            'file': {
                'instance': FileContentForm(),
                'action': reverse('courses:add_content_file')
            },
            'video': {
                'instance': VideoContentForm(),
                'action': reverse('courses:add_content_video')
            },
            'module': {
                'instance': ModuleCreateForm(),
                'action': reverse('courses:add_module', kwargs={'slug': context['object'].slug})
            }
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


class ModuleCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = ModuleCreateForm
    template_name = 'courses/module/create.html'

    def get_success_url(self):
        return reverse('courses:add_content', kwargs={'slug': self.kwargs.get('slug')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs.get('slug')
        course_qs = Course.objects.filter(owner=self.request.user)
        course = get_object_or_404(course_qs, slug=course_slug)
        context['course'] = course
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user

        slug = self.kwargs.get('slug')
        course_obj = get_object_or_404(Course, slug=slug)

        if user == course_obj.owner:
            form.instance.course = course_obj
            form.save()
        else:
            raise PermissionDenied()

        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response


class ModuleUpdateView(LoginRequiredMixin, IsTeacherMixin, UpdateView):
    form_class = ModuleCreateForm
    template_name = 'courses/module/edit.html'

    def get_success_url(self):
        obj = self.get_object()
        course = obj.course
        return reverse('courses:add_content', kwargs={'slug': course.slug})

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response


class ModuleDeleteView(LoginRequiredMixin, IsTeacherMixin, DeleteView):
    template_name = 'courses/module/delete.html'

    def get_success_url(self):
        obj = self.get_object()
        course = obj.course
        return reverse('courses:add_content', kwargs={'slug': course.slug})

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if request.is_ajax():
            data = {
                'message': 'Deleted',
            }
            return JsonResponse(data)
        else:
            return response


class ModuleShowHideView(LoginRequiredMixin, IsTeacherMixin, DetailView):
    http_method_names = 'post'

    def get_template_names(self):
        return []

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)

    def post(self, request, **_):
        obj = self.get_object()

        obj.visible = not obj.visible
        obj.save()

        if request.is_ajax():
            data = {
                'message': 'Success',
            }
            return JsonResponse(data)
        else:
            raise Exception("Ajax only")


class CourseManageDetailView(LoginRequiredMixin, IsTeacherMixin, DetailView):
    model = Course
    template_name = 'courses/course_main.html'

    def get_context_data(self, **kwargs):
        context = super(CourseManageDetailView, self).get_context_data(**kwargs)
        obj = context['object']
        participants = obj.participants.all()
        # last_activities = []
        # never_active = []
        # for p in participants:
        #     activities = CourseViewed.objects.filter(user=p, course=obj)
        #     if activities.exists():
        #         last = activities.first()
        #         last_activities.append({'user': p, 'last': last.timestamp})
        #     else:
        #         never_active.append({'user': p, 'last': None})
        # context['last_activities'] = sorted(last_activities, key=itemgetter('last'), reverse=True)
        # context['last_activities'] += never_active

        newest = CourseViewed \
            .objects.filter(user=OuterRef('pk')) \
            .order_by('-timestamp')
        activities = participants \
            .annotate(last=Subquery(newest.values('timestamp')[:1])) \
            .order_by(F('last').desc(nulls_last=True))

        context['last_activities'] = activities
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
