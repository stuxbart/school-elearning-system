from django import forms

class CourseUpdateForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput)
    overview = forms.CharField(widget=forms.Textarea)
    access_key = forms.CharField(widget=forms.TextInput)

    title.widget.attrs.update({'class': 'form-control'})
    overview.widget.attrs.update({'class': 'form-control'})
    access_key.widget.attrs.update({'class': 'form-control'})