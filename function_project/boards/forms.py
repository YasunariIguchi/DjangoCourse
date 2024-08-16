from django import forms
from .models import Theme, Comment


class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label="タイトル", required=True)
    class Meta:
        model = Theme
        fields = ("title",)

class EditThemeForm(forms.ModelForm):
    title = forms.CharField(label="タイトル", required=True)
    class Meta:
        model = Theme
        fields = ("title",)

class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(label="コメント", max_length=1000, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    class Meta:
        model = Comment
        fields = ("comment",)