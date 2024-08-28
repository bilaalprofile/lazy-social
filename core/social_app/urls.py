from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('add-post/', views.add_post, name="add_post"),
    path('delete-post/<str:page>/<int:pk>/', views.delete_post, name="delete_post"),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('login-user/', views.login_user, name='login_user'),
    path('logout-user/', views.logout_user, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
]
