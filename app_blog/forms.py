from django import forms
from .models import Blog


class MultiFileForm(forms.ModelForm):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 help_text='Ваши изображения', required=False)

    class Meta:
        model = Blog
        fields = ('topic', 'description', 'file_field')


class FileUpdateBlogsForm(forms.Form):
    file_field = forms.FileField()
