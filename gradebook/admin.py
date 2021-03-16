from django.contrib import admin

from .models import (
    StudentRecordBook,
    SubjectRecordBook,
    StudentSubjectRecordBook,
    Grade,
    Subject,
    Semestr
)

admin.site.register(StudentRecordBook)
admin.site.register(SubjectRecordBook)
admin.site.register(StudentSubjectRecordBook)
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Semestr)