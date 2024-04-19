from django import forms
from .models import Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MediaFile

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


        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['video', 'audio', 'eeg']
        widgets = {
            'video': forms.FileInput(attrs={'accept': '.mp4'}),
            'audio': forms.FileInput(attrs={'accept': '.wav'}),
            'EEG': forms.FileInput(attrs={'accept': '.mat'})
        }