from django import forms

from accounts.models import User

class UserChangePhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo']

class UserInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['info']