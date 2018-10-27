from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>', views.post_detail, name='post_detail'),
    path('<int:pk>/share/', views.post_share, name='post_share'),


]
