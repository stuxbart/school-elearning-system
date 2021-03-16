from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

class StudentRecordBookManager(models.Manager):
    def get_for_request(self, request):
        return self.get_queryset().filter(user=request.user)


class StudentRecordBook(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        related_name="record_books"
    )
    # year = models.CharField(max_length=10)
    repeated = models.BooleanField(default=False) # move to StudentSubjectRecordBook
    semestr = models.ForeignKey("Semestr", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    objects = StudentRecordBookManager()

    class Meta:
        get_latest_by = 'semestr__start'

    @property
    def passed(self):
        pass

    def __str__(self):
        if self.name:
            return self.name
        return f"Record book of {self.user} at semestr {self.semestr}"

    def get_max_ects_points(self):
        pass

    def get_current_ects_points(self):
        pass

    def get_avarage_grade(self):
        pass


class SubjectRecordBookManager(models.Manager):
    def get_for_request(self, request):
        return self.get_queryset().filter(instructor=request.user)


class SubjectRecordBook(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    subject = models.ForeignKey(
        "Subject", 
        on_delete=models.DO_NOTHING, 
        related_name="record_books"
    )
    semestr = models.ForeignKey("Semestr", on_delete=models.DO_NOTHING)
    instructor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    objects = SubjectRecordBookManager()

    @property
    def is_open(self):
        qs = self.students_record_books.filter(is_open=True)
        if qs.exists():
            return True
        return False

    def __str__(self):
        if self.name:
            return self.name
        return f"{self.subject} record book at semestr {self.semestr}"

    def get_absolute_url(self):
        return reverse("gradebook:teacher_gradebook_detail", kwargs={'pk': self.pk})


class StudentSubjectRecordBook(models.Model):
    student_record_book = models.ForeignKey(
        StudentRecordBook, 
        on_delete=models.DO_NOTHING,
        related_name="subjects_record_books"
    )
    subject_record_book = models.ForeignKey(
        SubjectRecordBook, 
        on_delete=models.DO_NOTHING,
        related_name="students_record_books"
    )
    
    paid = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    passed = models.BooleanField(default=False)
    
    final_grade_1 = models.ForeignKey(
        "Grade", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="final_grade_1_for"
    )
    final_grade_2 = models.ForeignKey(
        "Grade", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="final_grade_2_for"
    )
    final_grade_3 = models.ForeignKey(
        "Grade", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="final_grade_3_for"
    )

    def get_avarage_grade(self):
        weights = 0


class GradeManager(models.Manager):
    def get_for_request(self, request):
        return self.get_queryset().filter(created_by=request.user, student_subject_record_book__is_open=True)


class Grade(models.Model):
    student_subject_record_book = models.ForeignKey(
        StudentSubjectRecordBook, 
        on_delete=models.DO_NOTHING, 
        related_name="grades"
    )
    grade = models.CharField(max_length=10)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    weight = models.PositiveIntegerField()

    objects = GradeManager()

    def __str__(self):
        return f"{self.grade}: {self.student_subject_record_book.subject_record_book.subject} - {self.student_subject_record_book.student_record_book.user}"


SEMESTR_TYPE_CHOICES = (
    ('w', 'Winter'),
    ('s', 'Summer')
)
class Semestr(models.Model):
    year = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=SEMESTR_TYPE_CHOICES)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.get_type_display()} semestr, {self.year}"

class Subject(models.Model):
    name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=20)
    ects_points = models.PositiveIntegerField()

    def __str__(self):
        return self.name