from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...'
            })
        }


class SearchForm(forms.Form):
    q = forms.CharField(
        required=True,
        strip=True,
        min_length=2,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search..."
        })
    )