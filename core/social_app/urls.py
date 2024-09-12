from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friends, name='friends'),
    path('group-friends/', views.group_friends, name='group_friends'),
    path('add-post/', views.add_post, name="add_post"),
    path('delete-post/<str:page>/<int:pk>/',
         views.delete_post, name="delete_post"),
    path('edit_post/', views.edit_post, name="edit_post"),
    path('post-like/', views.post_like, name='post_like'),
    path('post_comments/',
         views.post_comments, name='post_comments'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('login-user/', views.login_user, name='login_user'),
    path('logout-user/', views.logout_user, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('fetch-comments/', views.fetch_comments, name="fetch_comments"),
    path("create-group/", views.create_group, name="create_group"),
    path('group/<int:pk>/', views.group, name="group"),
    path('join-group/<int:pk>/', views.join_group, name="join_group"),
    path('friend-request/', views.friend_request, name="friend_request"),
]
