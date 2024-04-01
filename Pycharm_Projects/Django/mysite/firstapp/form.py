from django import forms
from .models import MyModel,Book


class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['Domain', 'Age', 'Language']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']

