from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect
from django.views.generic import (
    ListView,
    FormView,
    DetailView,
    View,
    DeleteView,
    CreateView,
    UpdateView
)
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse, Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import F, Subquery, OuterRef

import json

from ..forms import (
    ImageContentForm,
    FileContentForm,
    VideoContentForm,
    ModuleCreateForm,
    AddUserToCourseForm,
    CourseCreateForm,
    TextContentCreateForm,
    TextUpdateForm
)

from ..mixins import IsTeacherMixin
from ..models import Course, Content, Module, Membership, Text

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
                'instance': TextContentCreateForm(),
                'action': reverse('courses:create_text_ajax'),
                'update_action': reverse('courses:update_text_ajax')
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


class TextContentCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = TextContentCreateForm
    template_name = 'courses/content/create.html'

    def get_success_url(self):
        course = self.object.module.course
        return reverse('courses:course_home', kwargs={'slug': course.slug})

    def get_context_data(self, **kwargs):
        module_pk = self.kwargs.get('pk')
        qs = Module.objects.filter(owner=self.request.user)
        module = get_object_or_404(qs, pk=module_pk)
        course = module.course
        context = super().get_context_data(**kwargs)
        context['module'] = module
        context['course'] = course
        return context

    def form_valid(self, form):
        user = self.request.user
        module_id = self.kwargs.get('pk')
        self.object = form.save(owner=user, module_id=module_id)
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'Text Created',
            }
            return JsonResponse(data)
        else:
            return response


class TextContentUpdateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = TextUpdateForm
    template_name = 'courses/content/update.html'

    def get_queryset(self):
        return Text.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return self.request.GET.get('next') or reverse('courses:text_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        text_id = self.kwargs.get('pk')
        text = get_object_or_404(self.get_queryset(), pk=text_id)
        # content = get_object_or_404(Content, item=text)
        return {
            'title': text.title,
            'content': text.content,
            # 'visible': content.visible
        }

    def form_valid(self, form):
        data = form.cleaned_data
        if self.request.is_ajax():
            content_id = data['content_id']
            content = get_object_or_404(Content, pk=content_id)
            text = content.item
            content.visible = data['visible']
            content.save()
        else:
            text_id = self.kwargs.get('pk')
            text = get_object_or_404(self.get_queryset(), pk=text_id)
            # content = get_object_or_404(Content, item=text)

        text.title = data['title']
        text.content = data['content']
        text.save()

        self.object = text

        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'Text Updated',
            }
            return JsonResponse(data)
        else:
            return response


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
    template_name = 'courses/course_main.html'

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

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


class CourseParticipantsManageDetailView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = AddUserToCourseForm
    template_name = 'courses/course_participants.html'

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        context['participants'] = Membership.objects.filter(course=course)
        return context

    def get_success_url(self):
        return reverse("courses:participants", kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        course_qs = self.get_queryset()
        course = get_object_or_404(course_qs, slug=self.kwargs['slug'])
        course.participants.set(form.cleaned_data['participants'], through_defaults={'method': 'owner'})
        return super().form_valid(form)


class ContentDeleteView(LoginRequiredMixin, IsTeacherMixin, DeleteView):
    template_name = 'courses/content/delete.html'

    def get_success_url(self):
        obj = self.get_object()
        course = obj.module.course
        return reverse('courses:add_content', kwargs={'slug': course.slug})

    def get_object(self, queryset=None):
        obj = get_object_or_404(Content, pk=self.kwargs.get('pk'))
        if obj.item.owner != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            return response


class ContentShowHideView(LoginRequiredMixin, IsTeacherMixin, SingleObjectMixin, View):
    http_method_names = 'post'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Content, pk=self.kwargs.get('pk'))
        if obj.item.owner != self.request.user:
            raise ObjectDoesNotExist()
        return obj

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


class ContentOrderView(LoginRequiredMixin, IsTeacherMixin, View):
    http_method_names = 'post'

    def post(self, request, **_):
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        pk = json_data.get('id')
        up_down = json_data.get('direction')

        content = get_object_or_404(Content, pk=pk)
        if content.item.owner != self.request.user:
            raise Http404

        if up_down == "up":
            content.move_up()
        elif up_down == "down":
            content.move_down()

        if request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            course = content.module.course
            return HttpResponseRedirect(reverse('courses:course_home', kwargs={'slug': course.slug}))


class ModuleOrderView(LoginRequiredMixin, IsTeacherMixin, View):
    http_method_names = 'post'

    def post(self, request, **_):
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        pk = json_data.get('id')
        up_down = json_data.get('direction')

        module = get_object_or_404(Module, pk=pk)
        if module.owner != self.request.user:
            raise Http404

        if up_down == "up":
            module.move_up()
        elif up_down == "down":
            module.move_down()

        if request.is_ajax():
            data = {
                'message': 'success',
            }
            return JsonResponse(data)
        else:
            course = module.course
            return HttpResponseRedirect(reverse('courses:course_home', kwargs={'slug': course.slug}))
