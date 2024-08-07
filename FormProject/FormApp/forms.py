from django import forms

class UserInfo(forms.Form):
    name = forms.CharField(label="名前", min_length=2, max_length=5)
    age = forms.IntegerField(label="年齢")
    mail = forms.EmailField(
        label="メールアドレス",
        widget=forms.TextInput(attrs={'placeholder': "bb@bbc.co.jp"})
        )
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