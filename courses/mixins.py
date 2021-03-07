from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from .models import (
    Course,
    CourseAdmin
)


class IsTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_teacher:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/')


# classes for path mixin
class PathText:
    def __init__(self, text):
        self.text = text
        self.type = 'text'

    def __str__(self):
        return self.text

class PathLink(PathText):
    def __init__(self, text, link):
        super().__init__(text=text)
        self.link = link
        self.type = 'link'

class PathMixin:
    """
    path = [
        PathLink('Some Page', reverse("app:page")),
        PathText('Some Text'),
    ]
    """

    pathe_template = "courses/snippets/path_breadcrumb.html"

    def get_paths(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if hasattr(self, 'paths'):
            p = self.paths
        else:
            p = self.get_paths()

        context['path'] = render_to_string(self.pathe_template, {'paths': p})
        return context


class ManageCoursesPathMixin(PathMixin):
    def get_paths(self):
        return [
            PathText("Home"),
            PathLink(
                "Manage Courses", 
                reverse_lazy("courses:manage_list")
            ),
        ]


class ManageCoursePathMixin(PathMixin):
    def get_paths(self):
        obj = self.get_object()
        return [
            PathText("Home"),
            PathLink(
                "Manage Courses", 
                reverse_lazy("courses:manage_list")
            ),
            PathLink(
                str(obj),
                reverse_lazy("courses:course_home", kwargs={
                    'slug': obj.slug
                    })
            ),
        ]


class ManageCourseContentPathMixin(ManageCoursePathMixin):
    def get_paths(self):
        paths = super().get_paths()
        obj = self.get_object()
        paths.append(PathLink(
            "Content",
            reverse_lazy("courses:add_content", kwargs={
                "slug": obj.slug
                })
        ))
        return paths


class ManageAdminsPathMixin(PathMixin):
    def get_paths(self):
        obj = self.get_object()
        if isinstance(obj, Course):
            name = str(obj)
            slug = obj.slug
        elif isinstance(obj, CourseAdmin):
            name = str(obj.course)
            slug = obj.course.slug
        else:
            raise TypeError()

        return [
            PathText("Home"),
            PathLink(
                "Manage Courses", 
                reverse_lazy("courses:manage_list")
            ),
            PathLink(
                name,
                reverse_lazy("courses:course_home", kwargs={
                    'slug': slug
                    })
            ),
            PathLink(
                "Admins",
                reverse_lazy("courses:admins", kwargs={
                    'slug': slug
                    })
            ),
        ]