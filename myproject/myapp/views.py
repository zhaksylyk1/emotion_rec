# from django.shortcuts import render

# Create your views here.
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .supabase_client import supabase
from .forms import VideoForm, RegisterForm 
from .models import Video
from .multimodal.prediction import prediction
from .functions.download_preporations import add_predictions_to_video
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import MediaFileForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

time_points = []
pred ={}

def login_or_signup_view(request):
    form_login = AuthenticationForm()
    form_signup = RegisterForm()
    if request.method == 'POST':
        if 'login_submit' in request.POST:  # If login form is submitted
            form_login = AuthenticationForm(request, data=request.POST)
            print("login")
            if form_login.is_valid():
                user = authenticate(request, username=form_login.cleaned_data['username'], password=form_login.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to home page after successful login
        if 'signup_submit' in request.POST:  # If signup form is submitted
            form_signup = RegisterForm(request.POST)
            print("signup")
            if form_signup.is_valid():
                print("signup valid")
                user = form_signup.save(commit=False)
                user.save()
                login(request, user)
                return redirect('home')  # Redirect to home page after successful signup
                
    return render(request, 'myapp/login.html', {'form_login': form_login, 'form_signup': form_signup})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            # Return an 'invalid login' error message
            return render(request, 'myapp/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'myapp/login.html')
    
def login_view2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            # Return an 'invalid login' error message
            return render(request, 'myapp/login2.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'myapp/ogin2.html')
    
def my_supabase_view(request):
    # Fetch data from Supabase
    data = supabase.table("test_1").select("*").execute()

    # Process the data as needed, and prepare it for the template
    context = {
        'data': data.data if data.data else []  # Ensuring data exists
    }

    # Render the template with the data
    return render(request, 'myapp/your_template.html', context)

def video_list(request ):
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            saved_video = form.save()  # Save the uploaded video
            directory_saved_video = os.path.dirname(saved_video.video.path)
            global time_points, pred
            time_points, pred = prediction(directory_saved_video)
            # form.save()
            # saved_video=form.save()
            # time_points=prediction(saved_video.video_file.path)
            
            return redirect('video_list')
    else:
        form = VideoForm()
    videos = Video.objects.all()  # Fetch all video objects from the database
    print(time_points)
    #time_points = [('Intro', 10, 15), ('Middle', 30, 40), ('End', 45, 47)]
    #time_points = [('Angry', 0, 1), ('Disgust', 1, 19), ('Happy', 19, 20), ('Disgust', 20, 43), ('Angry', 43, 44), ('Disgust', 44, 49), ('Angry', 49, 51), ('Happy', 51, 54), ('Disgust', 54, 55), ('Angry', 55, 55)]
    videos_exist = videos.exists()
    return render(request, 'myapp/video_list.html', {'videos': videos, 'time_points': time_points, 'form': form, 'videos_exist': videos_exist})

def delete_video(request, video_id):
    if request.method == 'POST':  # Ensure the request method is POST
        video = Video.objects.get(id=video_id)  # Get the video to delete
        video.delete()  # Delete the video
        return redirect('video_list')  # Redirect to the video list page
    
def save_video(request, video_id):
    if request.method == 'POST':  # Ensure the request method is POST
        video = Video.objects.get(id=video_id)  # Get the video to delete
        add_predictions_to_video(video_path=video.video.path, predictions=pred, output_folder="/Users/alikanafin/Desktop/emotion_recog_1/emotion_rec/myproject/media/output")
        return redirect('video_list')  # Redirect to the video list page

def upload_media_files(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('latest_media')  # Redirect to the same view to display the uploaded files or another success page
    else:
        form = MediaFileForm()
    return render(request, 'myapp/video_audio_eeg.html', {'form': form})

    
def login_or_signup_view(request):
    form_login = AuthenticationForm()
    form_signup = RegisterForm()
    if request.method == 'POST':
        if 'login_submit' in request.POST:  # If login form is submitted
            form_login = AuthenticationForm(request, data=request.POST)
            print("login")
            if form_login.is_valid():
                user = authenticate(request, username=form_login.cleaned_data['username'], password=form_login.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to home page after successful login
        if 'signup_submit' in request.POST:  # If signup form is submitted
            form_signup = RegisterForm(request.POST)
            print("signup")
            if form_signup.is_valid():
                print("signup valid")
                user = form_signup.save(commit=False)
                user.save()
                login(request, user)
                return redirect('home')  # Redirect to home page after successful signup
                
    return render(request, 'myapp/login.html', {'form_login': form_login, 'form_signup': form_signup})


def home(request):
    # Assuming you have a way to get the current user's name
    # You can replace "John Doe" with the actual username
    username = "John Doe"
    return render(request, 'myapp/home.html', {'username': username})

# def latest_media(request):
#     video_directory = os.path.join(settings.MEDIA_ROOT, 'videos')
#     videos = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith('.mp4')]
#     if not videos:
#         return HttpResponse('No video files found.', status=404)
    
#     latest_video = max(videos, key=os.path.getmtime)  # Get the latest video by modification time
#     video_url = os.path.join(settings.MEDIA_URL, 'videos', os.path.basename(latest_video))
    
#     return HttpResponse(f'<video controls><source src="{video_url}" type="video/mp4">Your browser does not support the video tag.</video>')

def latest_media(request):
    media_dir = 'media/videos'  # Set the directory where video files are stored
    videos = []
    try:
        # List all files in the media directory
        for filename in os.listdir(media_dir):
            if filename.endswith('.mp4'):  # Assuming we are only interested in mp4 files
                videos.append({
                    'url': f'/{media_dir}/{filename}',
                    'name': filename
                })
    except FileNotFoundError:
        videos = []  # No videos found or directory doesn't exist

    context = {
        'videos': videos,
        'videos_exist': len(videos) > 0
    }
    return render(request, 'myapp/eeg_pred.html', context)


