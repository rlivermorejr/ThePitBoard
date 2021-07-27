from django import forms


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2,
        'cols': 40,
        'autofocus': 'autofocus',
        'style': 'vertical-align: top'}),
        max_length=140, label="Post Content")
    post_content = forms.ImageField(required=False)


class CommentForm(forms.Form):
    text = forms.CharField(max_length=140)
