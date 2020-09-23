from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_form'),
    path('post/<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDelete.as_view(), name='post_confirm_delete'),
    path('<slug:slug>/comment/create/', views.comment_create, name='comment_form'),
    path('comment/<int:pk>/', views.comment_detail, name='comment_detail'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_confirm_delete'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.update_profile, name='profile'),
]
