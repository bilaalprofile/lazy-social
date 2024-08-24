from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import (
    Profile,
    Post
)


# Create your views here.

@login_required
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.order_by('-created_at')
    return render(request, 'social_app/index.html', {'profile': profile, 'posts': posts})


@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        country = request.POST.get('country')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        if image:
            profile.image = image
        profile.first_name = first_name
        profile.last_name = last_name
        profile.age = age
        profile.country = country
        profile.gender = gender
        profile.save()
        return redirect('profile')
    context = {
        "profile": profile,
        "posts": posts,
    }
    return render(request, 'social_app/profile.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        Post.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            image=request.FILES.get('image'),
        )
        return redirect('index')


@login_required
def delete_post(request, page, pk):
    Post.objects.get(id=pk).delete()
    return redirect(page)


def settings(request):
    return render(request, 'social_app/settings.html')


def change_password(request):
    message = ''
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password1')
        confirm_new_password = request.POST.get('password2')
        user = request.user
        if not user.check_password(old_password):
            message = 'old password is incorrect'
        elif new_password != confirm_new_password:
            message = 'new passwords not matching'
        elif len(new_password) < 8:
            message = 'password length must be 8 characters'
        else:
            user.set_password(new_password)
            user.save()
    return render(request, 'social_app/change_password.html', {"message": message})


def login_user(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            message = 'Incorrect Username or Password'

    return render(request, 'social_app/login_user.html', {'message': message})


def signup(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        country = request.POST.get('country')

        if User.objects.filter(username=username).exists():
            message = 'Username address already exists'

        elif len(password) < 8:
            message = 'password should be 8 characters'
        else:
            user = User.objects.create_user(
                username=username.lower(),
                password=password,

            )
            Profile.objects.create(user=user, first_name=first_name,
                                   last_name=last_name, age=age, gender=gender, country=country)
            user.save()

    return render(request, 'social_app/signup.html', {'message': message})


def logout_user(request):
    logout(request)
    return redirect('index')
