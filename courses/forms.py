from django import forms
from .models import Text, Image, File, Video, Module, Course, Content
from accounts.models import User


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'overview', 'access_key']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'overview': forms.Textarea(attrs={'class': 'form-control'}),
            'access_key': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TextContentForm(forms.ModelForm):
    visible = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['visible'].widget.attrs.update({'class': 'form-check-input'})

    module_id = forms.CharField(widget=forms.HiddenInput, required=False)
    content_id = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Text
        fields = ['title', 'content', 'visible']


class TextContentCreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea())
    visible = forms.BooleanField(required=False)
    module_id = forms.CharField(widget=forms.HiddenInput, required=False)
    content_id = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['visible'].widget.attrs.update({'class': 'form-check-input'})

    def save(self, owner=None, module_id=None):
        if owner is not None:
            data = self.cleaned_data
            item = Text(owner=owner, title=data['title'], content=data['content'])
            item.save()
            if module_id is not None:
                module = Module.objects.get(pk=module_id)
            else:
                module = Module.objects.get(pk=data['module_id'])
            content = Content(module=module, visible=data['visible'], item=item)
            content.save()
            return content


class TextUpdateForm(forms.ModelForm):
    content_id = forms.CharField(widget=forms.HiddenInput, required=False)
    visible = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['visible'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Text
        fields = ['title', 'content']


class ImageContentForm(forms.ModelForm):
    visible = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        # self.fields['file'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['visible'].widget.attrs.update({'class': 'form-control'})

    module_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Image
        fields = ['title', 'file', 'visible']


class FileContentForm(forms.ModelForm):
    visible = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        # self.fields['file'].widget.attrs.update({'class': 'custom-file-input'})
        self.fields['visible'].widget.attrs.update({'class': 'form-control'})

    module_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = File
        fields = ['title', 'file']


class VideoContentForm(forms.ModelForm):
    visible = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
        self.fields['visible'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].label = 'Video URL'

    module_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Video
        fields = ['title', 'file', 'visible']


class ModuleCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Module
        fields = ['title', 'description', 'visible']


class AddUserToCourseForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participants'].widget.attrs.update({'class': 'form-control', 'style': "max-height: 100px;"})

    class Meta:
        model = Course
        fields = ['participants']
