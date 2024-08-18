from django import forms
from .models import Book
from datetime import datetime

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "description", "price"]
        
    def save(self, *args, **kwargs):
        obj = super(BookForm, self).save(commit=False)
        obj.create_at = datetime.now()
        obj.update_at = datetime.now()
        obj.save()
        return obj

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["name", "description", "price"]
        
    def save(self, *args, **kwargs):
        obj = super(BookUpdateForm, self).save(commit=False)
        obj.update_at = datetime.now()
        obj.save()
        return obj