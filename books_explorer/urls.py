# Create url patterns for the views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('<uuid:file_uuid>', views.render_one_file, name='single_file'),
]
