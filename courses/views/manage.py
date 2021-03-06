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
from django.contrib.contenttypes.models import ContentType

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
    CourseAdminCreateForm,
    CourseAdminUpdateForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_courses'] = self.request.user.courseadmin_set.all()
        return context


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

    def get_object(self):
        slug = self.kwargs['slug']

        qs = self.get_queryset()
        obj = qs.filter(slug=slug)
        if obj.exists():
            return obj.first()

        qs = self.request.user.admin_courses.all()
        obj = qs.filter(slug=slug)
        if obj.exists():
            obj = obj.first()
            if obj.can_edit_course(self.request.user):
                return obj
        
        raise Http404()
        
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

    def get_object(self):
        slug = self.kwargs['slug']
        user = self.request.user

        qs = self.get_queryset()
        obj = qs.filter(slug=slug, owner=user)
        if obj.exists():
            return obj.first()

        qs = user.admin_courses.all()
        obj = qs.filter(slug=slug)
        if obj.exists():
            obj = obj.first()
            if obj.can_edit_content(user):
                return obj
        raise Http404()

    def get_context_data(self, **kwargs):
        context = super(CourseAddContentView, self).get_context_data(**kwargs)
        course = self.get_object()
        context["forms"] = {
            'text': {
                'instance': TextContentCreateForm(),
                'action': reverse('courses:create_text_ajax', kwargs={'slug': course.slug}),
                'update_action': reverse('courses:update_text_ajax')
            },
            'image': {
                'instance': ImageContentCreateForm(),
                'action': reverse('courses:create_image_ajax', kwargs={'slug': course.slug}),
                'update_action': reverse('courses:update_image_ajax')
            },
            'file': {
                'instance': FileContentCreateForm(),
                'action': reverse('courses:create_file_ajax', kwargs={'slug': course.slug}),
                'update_action': reverse('courses:update_file_ajax')
            },
            'video': {
                'instance': VideoContentCreateForm(),
                'action': reverse('courses:create_video_ajax', kwargs={'slug': course.slug}),
                'update_action': reverse('courses:update_video_ajax')
            },
            'module': {
                'instance': ModuleCreateForm(),
                'action': reverse('courses:add_module', kwargs={'slug': course.slug})
            }
        }
        return context


class BaseContentCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    template_name = 'courses/content/create.html'
    success_message = "Created"

    def get_success_url(self):
        course = self.object.course
        return reverse('courses:course_home', kwargs={'slug': course.slug})

    def get_course(self):
        slug = self.kwargs['slug']
        user = self.request.user

        qs = Course.objects.all()
        obj = qs.filter(slug=slug, owner=user)
        if obj.exists():
            return obj.first()

        qs = user.admin_courses.all()
        obj = qs.filter(slug=slug)
        if obj.exists():
            obj = obj.first()
            if obj.can_edit_content(user):
                return obj
        raise Http404("Course does not exist")

    def get_module(self):
        course = self.get_course()

        module_pk = self.kwargs.get('pk') or self.request.POST.get('module_id')
        qs = Module.objects.filter(
            id=module_pk,
            course=course
        )

        if qs.exists():
            module = qs.first()
        else:
            raise Http404("Module does not exist")
        return module

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.get_course()
        context['course'] = self.get_module()
        return context

    def form_valid(self, form):
        user = self.request.user
        course = self.get_course()
        module = self.get_module()

        self.object = form.save(
            owner=user, 
            module=module, 
            course=course
        )
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


class BaseContentUpdateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    template_name = 'courses/content/update.html'
    SUCCESS_MESSAGE = "Success"
    ERROR_MESSAGE = "Error"

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(self.model)
        return Content.objects.filter(
            owner=self.request.user,
            content_type=content_type
        )

    def get_object(self):
        if self.request.is_ajax():
            content_id = self.request.POST.get('content_id')
        else:
            content_id = self.kwargs.get('pk')

        content = get_object_or_404(self.get_queryset(), pk=content_id)
        return content

    def get_initial(self):
        initial = super().get_initial()
        content = self.get_object()

        initial.update({
            'visible': content.visible
        })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj = self.get_object()
        kwargs.update({'instance': obj.item})
        return kwargs
        

    def form_valid(self, form):
        data = form.cleaned_data

        content = self.get_object()
        content.visible = data['visible']
        content.save()

        self.object = content.item
        form.save()

        if self.request.is_ajax():
            return JsonResponse({'message': self.SUCCESS_MESSAGE,})
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'message': self.ERROR_MESSAGE,})
        else:
            return super().form_valid(form)


class TextContentUpdateView(BaseContentUpdateView):
    form_class = TextUpdateForm
    model = Text

    SUCCESS_MESSAGE = "Text updated successfully"
    ERROR_MESSAGE = "An error occured"

    def get_success_url(self):
        return reverse('courses:text_detail', kwargs={'pk': self.object.pk})
    


class ImageContentUpdateView(BaseContentUpdateView):
    form_class = ImageUpdateForm
    model = Image

    SUCCESS_MESSAGE = "Image updated successfully"
    ERROR_MESSAGE = "An error occured"

    def get_success_url(self):
        return reverse('courses:image_detail', kwargs={'pk': self.object.pk})


class FileContentUpdateView(BaseContentUpdateView):
    form_class = FileUpdateForm
    model = File

    SUCCESS_MESSAGE = "File updated successfully"
    ERROR_MESSAGE = "An error occured"

    def get_success_url(self):
        return reverse('courses:file_detail', kwargs={'pk': self.object.pk})


class VideoContentUpdateView(BaseContentUpdateView):
    form_class = VideoUpdateForm
    model = Video
    
    SUCCESS_MESSAGE = "Video updated successfully"
    ERROR_MESSAGE = "An error occured"

    def get_success_url(self):
        return reverse('courses:video_detail', kwargs={'pk': self.object.pk})

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
    form_class = CourseAdminCreateForm
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
        context['course'] = course
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


class CourseAdminDeleteView(IsTeacherMixin, LoginRequiredMixin, DeleteView):
    template_name = 'courses/delete.html'

    def get_queryset(self):
        allowed_courses = Course.objects.filter(owner=self.request.user)
        return CourseAdmin.objects.filter(course__in=allowed_courses)

    def get_object(self):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=self.kwargs['pk'], course__slug=self.kwargs['slug'])
        return obj
    
    def get_success_url(self):
        return reverse("courses:admins", kwargs={'slug': self.kwargs['slug']})


class CourseAdminUpdateView(IsTeacherMixin, LoginRequiredMixin, UpdateView):
    template_name = "courses/course_admin_update.html"
    form_class = CourseAdminUpdateForm

    def get_queryset(self):
        allowed_courses = Course.objects.filter(owner=self.request.user)
        return CourseAdmin.objects.filter(course__in=allowed_courses)

    def get_object(self):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=self.kwargs['pk'], course__slug=self.kwargs['slug'])
        return obj

    def get_success_url(self):
        return reverse("courses:admins", kwargs={'slug': self.kwargs['slug']})