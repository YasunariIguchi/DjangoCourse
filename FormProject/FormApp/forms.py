from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from django.core import validators
from .models import Post, User

def check_name(value):
    if value == "aaaaa":
        raise validators.ValidationError("その名前は禁止だお")


class UserInfo(forms.Form):
    name = forms.CharField(label="名前", min_length=2, max_length=5, validators=[check_name])
    age = forms.IntegerField(label="年齢", validators=[validators.MinValueValidator(20, message="20以上にするお")])
    mail = forms.EmailField(
        label="メールアドレス",
        widget=forms.TextInput(attrs={
            'class': 'mail-class',
            'placeholder': "bb@bbc.co.jp"
        }))
    verify_mail = forms.EmailField(
        label="メールアドレス再入力",
        widget=forms.TextInput(attrs={
            'class': 'mail-class',
            'placeholder': "bb@bbc.co.jp"
        }))
    is_married = forms.BooleanField(label="結婚済", initial=True, required=False)
    birthday = forms.DateField(label="誕生日", initial="1990-01-01")
    salary = forms.DecimalField(label="年収")
    job = forms.ChoiceField(label="職業", choices=(
        (1, "正社員"),
        (2, "自営業"),
        (3, "学生"),
        (4, "無職")
    ), widget=forms.RadioSelect)
    hobbies = forms.MultipleChoiceField(label="趣味", choices=(
        (1, "スポーツ"),
        (2, "映画鑑賞"),
        (3, "読書"),
        (4, "その他")
    ), widget=forms.CheckboxSelectMultiple)
    homepage = forms.URLField(label="ホームページ", required=False)
    memo = forms.CharField(widget=forms.Textarea)
    
    def clean_hobbies(self):
        data = self.cleaned_data.get('hobbies')
        if not data:
            raise forms.ValidationError("少なくとも1つの趣味を選択してください。")
        return data
    
    def __init__(self, *args, **kwargs):
        super(UserInfo, self).__init__(*args, **kwargs)
        self.fields['job'].widget.attrs['id'] = 'id_job'
        self.fields['hobbies'].widget.attrs['class'] = 'hobbies_class'
        
    def clean_homepage(self):
        homepage = self.cleaned_data['homepage']
        if not homepage.startswith('https'):
            raise forms.ValidationError('ホームページのURLはhttpsのみだお')
        
    def clean(self):
        cleaned_data = super().clean()
        mail = cleaned_data['mail']
        verify_mail = cleaned_data['verify_mail']
        if mail != verify_mail:
            raise forms.ValidationError("メールアドレスが一致しないお")
            
class BaseForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        print(f"From: {self.__class__.__name__}実行")
        return super(BaseForm, self).save(*args, **kwargs)
class PostModelForm(BaseForm):
    name = forms.CharField(label="名前")
    title = forms.CharField(label="タイトルだお")
    memo = forms.CharField(label="メモ",
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 50})
    )
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ["name", "title"]
        # exclude = ["title"]
    
    def save(self, *args, **kwagrs):
        obj = super().save(commit=False, *args, **kwagrs)
        obj.name = obj.name.upper()
        obj.save()
        print(type(obj))
        print("save実行")
        return obj

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "ああああ":
            raise validators.ValidationError("その名前は禁止されていますお。")
        return name
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title == "かかかか":
            raise validators.ValidationError("そのタイトルは禁止されていますお。")
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if Post.objects.filter(title=title).exists():
            raise validators.ValidationError("そのタイトルは存在するお")
        return cleaned_data

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'