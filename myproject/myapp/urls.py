from django.urls import path
from . import views
from myapp.views import my_supabase_view

urlpatterns = [
    path('', views.login_or_signup_view, name='login'),
    path('login2/', views.login_view2, name='login2'),
    path('supabase-data/', my_supabase_view, name='supabase_data'),
    path('upload/', views.video_list, name='video_list'),  # For listing videos
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('save/<int:video_id>/', views.save_video, name='save_video'),
    path('upload2/', views.upload_media_files, name='video_audio_eeg'),
    path('av_eeg/', views.latest_media, name='latest_media'),
]
