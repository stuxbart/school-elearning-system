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
    ModuleCreateForm,
    AddUserToCourseForm,
    CourseCreateForm,
    TextContentCreateForm,
    TextUpdateForm,
    ImageContentCreateForm,
    ImageUpdateForm,
    VideoContentCreateForm,
    VideoUpdateForm,
    FileContentCreateForm,
    FileUpdateForm,
    AddAdminsToCourseForm,
    CourseAdminForm
)

from ..mixins import IsTeacherMixin
from ..models import (
    Course,
    Content,
    Module,
    Membership,
    CourseAdmin,
    Text,
    Image,
    File,
    Video
)

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
                'instance': ImageContentCreateForm(),
                'action': reverse('courses:create_image_ajax'),
                'update_action': reverse('courses:update_image_ajax')
            },
            'file': {
                'instance': FileContentCreateForm(),
                'action': reverse('courses:create_file_ajax'),
                'update_action': reverse('courses:update_file_ajax')
            },
            'video': {
                'instance': VideoContentCreateForm(),
                'action': reverse('courses:create_video_ajax'),
                'update_action': reverse('courses:update_video_ajax')
            },
            'module': {
                'instance': ModuleCreateForm(),
                'action': reverse('courses:add_module', kwargs={'slug': context['object'].slug})
            }
        }
        return context


class BaseContentCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    template_name = 'courses/content/create.html'
    success_message = "Created"

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
                'message': self.success_message,
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():

            data = {
                'message': 'error',
            }
            return JsonResponse(data)
        else:
            return response


class TextContentCreateView(BaseContentCreateView):
    form_class = TextContentCreateForm
    success_message = "Text created"


class ImageContentCreateView(BaseContentCreateView):
    form_class = ImageContentCreateForm
    success_message = "Image created"


class FileContentCreateView(BaseContentCreateView):
    form_class = FileContentCreateForm
    success_message = "File created"


class VideoContentCreateView(BaseContentCreateView):
    form_class = VideoContentCreateForm
    success_message = "Video created"

# class TextContentCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
#     form_class = TextContentCreateForm
#     template_name = 'courses/content/create.html'
#
#     def get_success_url(self):
#         course = self.object.module.course
#         return reverse('courses:course_home', kwargs={'slug': course.slug})
#
#     def get_context_data(self, **kwargs):
#         module_pk = self.kwargs.get('pk')
#         qs = Module.objects.filter(owner=self.request.user)
#         module = get_object_or_404(qs, pk=module_pk)
#         course = module.course
#         context = super().get_context_data(**kwargs)
#         context['module'] = module
#         context['course'] = course
#         return context
#
#     def form_valid(self, form):
#         user = self.request.user
#         module_id = self.kwargs.get('pk')
#         self.object = form.save(owner=user, module_id=module_id)
#         response = super().form_valid(form)
#         if self.request.is_ajax():
#             data = {
#                 'message': 'Text Created',
#             }
#             return JsonResponse(data)
#         else:
#             return response
#
#     def form_invalid(self, form):
#         response = super().form_invalid(form)
#         if self.request.is_ajax():
#
#             print(form.cleaned_data)
#             data = {
#                 'message': 'error',
#             }
#             return JsonResponse(data)
#         else:
#             return response


class TextContentUpdateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = TextUpdateForm
    template_name = 'courses/content/update.html'

    def get_queryset(self):
        return Text.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return self.request.GET.get('next') or reverse('courses:text_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        if not self.request.is_ajax():
            text_id = self.kwargs.get('pk')
            text = get_object_or_404(self.get_queryset(), pk=text_id)
            # content = get_object_or_404(Content, item=text)
            return {
                'title': text.title,
                'content': text.content,
                # 'visible': content.visible
            }
        else:
            return {}

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

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'message': 'error',
            }
            return JsonResponse(data)
        else:
            return response


class ImageContentUpdateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = ImageUpdateForm
    template_name = 'courses/content/update.html'

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return self.request.GET.get('next') or reverse('courses:image_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        if not self.request.is_ajax():
            image_id = self.kwargs.get('pk')
            image = get_object_or_404(self.get_queryset(), pk=image_id)
            # content = get_object_or_404(Content, item=image)
            return {
                'title': image.title,
                'file': image.file,
                # 'visible': content.visible
            }
        else:
            return {}

    def form_valid(self, form):
        data = form.cleaned_data
        if self.request.is_ajax():
            content_id = data['content_id']
            content = get_object_or_404(Content, pk=content_id)
            image = content.item
            content.visible = data['visible']
            content.save()
        else:
            image_id = self.kwargs.get('pk')
            image = get_object_or_404(self.get_queryset(), pk=image_id)
            # content = get_object_or_404(Content, item=image)

        image.title = data['title']
        image.file = data['file']
        image.save()

        self.object = image

        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'Image Updated',
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'message': 'error',
            }
            return JsonResponse(data)
        else:
            return response


class FileContentUpdateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = FileUpdateForm
    template_name = 'courses/content/update.html'

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return self.request.GET.get('next') or reverse('courses:file_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        if not self.request.is_ajax():
            file_id = self.kwargs.get('pk')
            file = get_object_or_404(self.get_queryset(), pk=file_id)
            # content = get_object_or_404(Content, item=file)
            return {
                'title': file.title,
                'file': file.file,
                # 'visible': content.visible
            }
        else:
            return {}

    def form_valid(self, form):
        data = form.cleaned_data
        if self.request.is_ajax():
            content_id = data['content_id']
            content = get_object_or_404(Content, pk=content_id)
            file = content.item
            content.visible = data['visible']
            content.save()
        else:
            file_id = self.kwargs.get('pk')
            file = get_object_or_404(self.get_queryset(), pk=file_id)
            # content = get_object_or_404(Content, item=video)

        file.title = data['title']
        file.file = data['file']
        file.save()

        self.object = file

        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'File Updated',
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'message': 'error',
            }
            return JsonResponse(data)
        else:
            return response


class VideoContentUpdateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = VideoUpdateForm
    template_name = 'courses/content/update.html'

    def get_queryset(self):
        return Video.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return self.request.GET.get('next') or reverse('courses:video_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        if not self.request.is_ajax():
            video_id = self.kwargs.get('pk')
            video = get_object_or_404(self.get_queryset(), pk=video_id)
            # content = get_object_or_404(Content, item=video)
            return {
                'title': video.title,
                'file': video.file,
                # 'visible': content.visible
            }
        else:
            return {}

    def form_valid(self, form):
        data = form.cleaned_data
        if self.request.is_ajax():
            content_id = data['content_id']
            content = get_object_or_404(Content, pk=content_id)
            video = content.item
            content.visible = data['visible']
            content.save()
        else:
            video_id = self.kwargs.get('pk')
            video = get_object_or_404(self.get_queryset(), pk=video_id)
            # content = get_object_or_404(Content, item=video)

        video.title = data['title']
        video.file = data['file']
        video.save()

        self.object = video

        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': 'Video Updated',
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'message': 'error',
            }
            return JsonResponse(data)
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
        course_qs = self.get_queryset()
        course = get_object_or_404(course_qs, slug=self.kwargs['slug'])
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


class CourseAdminsManageDetailView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = CourseAdminForm
    template_name = 'courses/course_admins.html'
    prefix = "1"

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

    def get_object(self):
        course_qs = self.get_queryset()
        return get_object_or_404(course_qs, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['admins'] = CourseAdmin.objects.filter(course=course)
        return context

    def get_success_url(self):
        return reverse("courses:admins", kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        return {
            'course': self.get_object()
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'course': self.get_object()})
        return kwargs
    
    def post(self, request, *args, **kwargs):
        forms_count = int(self.request.POST.get('count', 1))
        all_valid = True
        valid_forms = []

        for i in range(1, forms_count+1):
            self.prefix = i
            form = self.get_form()

            if form.is_valid():
                valid_forms.append(form)
            else:
                all_valid = False
                break

        if all_valid:
            for i in valid_forms:
                i.save()

        if all_valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)