from django import forms
from courses.models import Text, Image, File, Video

class CourseUpdateForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput)
    overview = forms.CharField(widget=forms.Textarea)
    access_key = forms.CharField(widget=forms.TextInput)

    title.widget.attrs.update({'class': 'form-control'})
    overview.widget.attrs.update({'class': 'form-control'})
    access_key.widget.attrs.update({'class': 'form-control'})

class TextContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})

    module_id = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Text
        fields = ['title', 'content']
    
class ImageContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        # self.fields['file'].widget.attrs.update({'class': 'custom-file-input'})

    module_id = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Image
        fields = ['title', 'file']

class FileContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        # self.fields['file'].widget.attrs.update({'class': 'custom-file-input'})

    module_id = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = File
        fields = ['title', 'file']

class VideoContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].label = 'Video URL'

    module_id = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Video
        fields = ['title', 'file']