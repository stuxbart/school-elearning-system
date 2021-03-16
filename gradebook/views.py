from django.views.generic import (
    DetailView, 
    View, 
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.shortcuts import (
    get_object_or_404, 
    HttpResponse, 
    Http404, 
    reverse
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    StudentRecordBook, 
    SubjectRecordBook, 
    StudentSubjectRecordBook, 
    Grade
)
from .forms import GradeCreateForm, GradeUpdateForm

from courses.mixins import (
    IsTeacherMixin, 
    PathLink, 
    PathText, 
    PathMixin
)

class StudentRecordBookDetailView(PathMixin, LoginRequiredMixin, DetailView):
    template_name = "gradebook/studentrecordbook_detail.html"

    def get_paths(self):
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:user_home")
            ),
        ]

    def get_queryset(self):
        return StudentRecordBook.objects.get_for_request(self.request)

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        qs = self.get_queryset()
        if pk:
            obj = get_object_or_404(self.get_queryset(), pk=pk)
        elif qs.exists():
            obj = qs.latest()
        else:
            raise Http404("Record books not found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record_books'] = self.get_queryset()

        return context


class TeacherRecordBookListView(PathMixin, IsTeacherMixin ,LoginRequiredMixin, ListView):
    template_name = "gradebook/teacher_list.html"

    def get_paths(self):
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:teacher_home")
            ),
        ]

    def get_queryset(self):
        return SubjectRecordBook.objects.get_for_request(self.request)


class TeacherRecordBookDetailView(PathMixin, IsTeacherMixin ,LoginRequiredMixin, DetailView):
    template_name = "gradebook/teacher_detail.html"

    def get_paths(self):
        obj = self.get_object()
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:teacher_home")
            ),
            PathLink(
                str(obj.subject), 
                reverse_lazy("gradebook:teacher_gradebook_detail", kwargs={'pk': obj.id})
            ),
        ]

    def get_queryset(self):
        return SubjectRecordBook.objects.get_for_request(self.request)


class GradeCreateView(PathMixin, IsTeacherMixin, LoginRequiredMixin, CreateView):
    template_name = "gradebook/create_grade.html"
    form_class = GradeCreateForm

    def get_paths(self):
        obj = self.get_object()
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:teacher_home")
            ),
            PathLink(
                str(obj.subject_record_book.subject), 
                reverse_lazy("gradebook:teacher_gradebook_detail", kwargs={'pk': obj.subject_record_book.id})
            ),
            PathText(obj.student_record_book.user.full_name),
            PathText("Add Grade")
        ]

    def get_queryset(self):
        return StudentSubjectRecordBook.objects.all()

    def get_object(self):
        record_book_id = self.kwargs.get('pk')
        user = self.request.user
        qs = self.get_queryset()

        return get_object_or_404(qs, 
            pk=record_book_id, 
            subject_record_book__instructor=user,
            is_open=True
        )

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        obj = self.get_object()

        initial.update({
            "student_subject_record_book": obj.id,
            "created_by": user.id
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'endpoint': reverse('gradebook:create_grade', kwargs={'pk':self.kwargs.get('pk')}),
            'object': self.get_object()
        })
        return context

    def get_success_url(self):
        record_book_id = self.kwargs.get('pk')
        student_subject_record_book = get_object_or_404(StudentSubjectRecordBook, pk=record_book_id)

        return reverse("gradebook:teacher_gradebook_detail", kwargs={
            'pk': student_subject_record_book.subject_record_book.id
        })


class GradeUpdateView(PathMixin, IsTeacherMixin, LoginRequiredMixin, UpdateView):
    template_name = "gradebook/update_grade.html"
    form_class = GradeUpdateForm

    def get_paths(self):
        obj = self.get_object()
        stu_sub = obj.student_subject_record_book
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:teacher_home")
            ),
            PathLink(
                str(stu_sub.subject_record_book.subject), 
                reverse_lazy("gradebook:teacher_gradebook_detail", kwargs={'pk': stu_sub.subject_record_book.id})
            ),
            PathText(stu_sub.student_record_book.user.full_name),
            PathText("Update Grade")
        ]

    def get_queryset(self):
        return Grade.objects.get_for_request(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'endpoint': reverse('gradebook:update_grade', kwargs={'pk':self.kwargs.get('pk')})
        })
        return context

    def get_success_url(self):
        grade = self.get_object()

        return reverse("gradebook:detail_grade", kwargs={
            'pk': grade.id
        })

class GradeDeleteView(PathMixin, IsTeacherMixin, LoginRequiredMixin, DeleteView):
    template_name = "gradebook/delete_grade.html"

    def get_paths(self):
        obj = self.get_object()
        stu_sub = obj.student_subject_record_book
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:teacher_home")
            ),
            PathLink(
                str(stu_sub.subject_record_book.subject), 
                reverse_lazy("gradebook:teacher_gradebook_detail", kwargs={'pk': stu_sub.subject_record_book.id})
            ),
            PathText(stu_sub.student_record_book.user.full_name),
            PathText("Delete Grade")
        ]

    def get_queryset(self):
        return Grade.objects.get_for_request(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'endpoint': reverse('gradebook:delete_grade', kwargs={'pk':self.kwargs.get('pk')})
        })
        return context

    def get_success_url(self):
        grade = self.get_object()

        return reverse("gradebook:teacher_gradebook_detail", kwargs={
            'pk': grade.student_subject_record_book.subject_record_book.id
        })


class GradeDetailView(PathMixin, IsTeacherMixin, LoginRequiredMixin, DetailView):
    template_name = "gradebook/detail_grade.html"

    def get_paths(self):
        obj = self.get_object()
        stu_sub = obj.student_subject_record_book
        return [
            PathText("Home"),
            PathLink(
                "Gradebook", 
                reverse_lazy("gradebook:teacher_home")
            ),
            PathLink(
                str(stu_sub.subject_record_book.subject), 
                reverse_lazy("gradebook:teacher_gradebook_detail", kwargs={'pk': stu_sub.subject_record_book.id})
            ),
            PathText(stu_sub.student_record_book.user.full_name),
            PathText("Detail Grade")
        ]

    def get_queryset(self):
        return Grade.objects.get_for_request(self.request)


