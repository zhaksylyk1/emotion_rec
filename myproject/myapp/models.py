from django.db import models
from .multimodal.prediction import prediction
# Create your models here.
from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    description = models.TextField(blank=True) 
    
    # Optionally, add more fields such as description, timestamps, etc.
    
    def delete(self, *args, **kwargs):
        # You have to prepare the path to your file
        # Here we are using the 'path' attribute of the FileField
        storage, path = self.video.storage, self.video.path
        # Delete the model before the file
        print(path)
        super().delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]