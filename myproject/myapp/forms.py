from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Title', 'class': 'form-control'}
        ),
        label=''  # This ensures that the label is not displayed
    )
    video = forms.FileField(
        widget=forms.FileInput(
            attrs={'id': 'video', 'hidden': True}
        ),
        label=''  # This ensures that the label is not displayed
    )

    class Meta:
        model = Video
        fields = ['title', 'video']