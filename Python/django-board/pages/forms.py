from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    #  Form 에 대한 정보들 입력
    title = forms.CharField(
        max_length=20,
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'title',
                'placeholder': 'Enter the title',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'cols': 50,
                'placeholder': 'Enter the content',
                'class': 'content-type',
            }
        )
    )

    #  Model 의 대한 정보들 입력
    class Meta:
        model = Post
        fields = ('title', 'content', )
