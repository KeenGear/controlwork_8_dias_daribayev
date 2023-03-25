from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'review']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a review...'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('This field is required.')
        elif image.size > 4 * 1024 * 1024:
            raise forms.ValidationError('Image file size should not exceed 4 MB.')
        elif not image.content_type.startswith('image/'):
            raise forms.ValidationError('Invalid file format. Only image files are allowed.')
        return image

    def clean_review(self):
        review = self.cleaned_data.get('review')
        if not review:
            raise forms.ValidationError('This field is required.')
        elif len(review) > 1000:
            raise forms.ValidationError('Review should not exceed 1000 characters.')
        return review


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
