from django import forms
from django.contrib.auth import get_user_model
from .models import Grade, StudentSubjectRecordBook

User = get_user_model()

class GradeCreateForm(forms.ModelForm):
    student_subject_record_book = forms.ModelChoiceField(
        widget=forms.HiddenInput, 
        disabled=True,
        queryset=StudentSubjectRecordBook.objects.all()
    )
    created_by = forms.ModelChoiceField(
        widget=forms.HiddenInput, 
        disabled=True,
        queryset=User.objects.all()
        )

    class Meta:
        model = Grade
        fields = ["student_subject_record_book", "grade", "description", "created_by", "weight"]



class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["grade", "description", "weight"]