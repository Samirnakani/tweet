
from django.contrib import admin
from django.urls import path,include
from tweet import views


urlpatterns = [
    path('',views.home,name="home"),
    path('create/',views.tweet_create,name="tweet_create"),
    path('edit/<int:tweet_id>/',views.tweet_edit,name="tweet_edit"),
    path("delete/<int:tweet_id>/", views.tweet_delete, name="tweet_delete"),
    # In your urls.py
path('tweet/<int:tweet_id>/detail/', views.tweet_detail_ajax, name='tweet_detail_ajax'),
    
] 