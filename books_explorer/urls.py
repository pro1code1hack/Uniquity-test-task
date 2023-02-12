# Create url patterns for the views
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('upload_file/', (views.UploadFileView.as_view(template_name='upload_file.html')), name='upload_file'),
    path('', (views.HomeView.as_view(template_name='home.html')), name='home'),
    path('<uuid:file_uuid>', views.RenderOneFileView.as_view(), name='single_file'),
]
