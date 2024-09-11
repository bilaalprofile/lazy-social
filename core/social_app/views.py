from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import (
    Profile,
    Post,
    Like,
    Comment,
    SocialGroup
)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.

@login_required
def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    groups = SocialGroup.objects.all()
    posts = Post.objects.order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.is_liked_by_user(request.user)
    context = {
        'posts': posts,
        'profile': profile,
        'groups': groups,
    }
    return render(request, 'social_app/index.html', context)


@login_required
def profile(request):
    groups = SocialGroup.objects.all()
    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    for post in posts:
        post.liked_by_user = post.is_liked_by_user(request.user)
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
        'groups': groups,

    }
    return render(request, 'social_app/profile.html', context)


@login_required
def create_group(request):
    if request.method == "POST":
        print(request.POST)
        group = SocialGroup.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            image=request.FILES.get('image'),
            description=request.POST.get('description'),
        )
        group.members.add(request.user)
    return redirect('group', group.id)


@login_required
def group(request, pk):
    group = get_object_or_404(SocialGroup, id=pk)
    posts = Post.objects.filter(group=group)
    for post in posts:
        post.liked_by_user = post.is_liked_by_user(request.user)
    has_joined = group.members.filter(username=request.user.username).exists()
    return render(request, 'social_app/group.html', {'group': group, 'has_joined': has_joined, 'posts': posts})

def edit_group(request):
    return redirect("group", group.id)

def join_group(request, pk):
    request_type = request.GET.get('type')
    group = get_object_or_404(SocialGroup, id=pk)
    if request_type == 'join':
        group.members.add(request.user)
        message = "removed from"
    else:
        group.members.remove(request.user)
        message = "added to"
    return JsonResponse({'status': 'success', 'message': f'You have successfully been {message} the group'})


def group_friends(request):
    members = SocialGroup.objects.all()
    return render(request, "social_app/group_friends.html", {'members': members})


@login_required
def friends(request):
    return render(request, 'social_app/friends.html')


@login_required
def add_post(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id', None)
        if group_id:
            group = SocialGroup.objects.get(id=group_id)
        Post.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            group=group,
            image=request.FILES.get('image'),
        )
        return redirect('index')


@login_required
def edit_post(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        page = request.POST.get('page')
        post = Post.objects.get(id=id)
        post.body = request.POST.get('body')
        post.image = request.FILES.get('image')
        post.save()
        return redirect(page)


@login_required
def delete_post(request, page, pk):
    Post.objects.get(id=pk).delete()
    return redirect(page)


@login_required
def post_like(request):
    post_id = request.GET.get('id')
    post = get_object_or_404(Post, id=request.GET.get('id'))
    post = Post.objects.get(id=post_id)
    user = request.user

    # Check if the user has already liked the post
    liked = False
    like = Like.objects.filter(user=user, post=post).first()
    print(like, type(like))

    if like:
        like.delete()
        message = "You unliked this post."
    else:
        Like.objects.create(user=user, post=post)
        liked = True
        message = "You liked this post."

    response_data = {
        "liked": liked,
        "total_likes": post.likes.count(),
        "message": message,
    }

    return JsonResponse(response_data)


def post_comments(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    body = request.POST.get('comment')
    image = request.FILES.get('image')
    print(request.POST)
    if body or image:
        Comment.objects.create(
            post=post,
            body=body,
            image=image
        )
    else:
        pass
    return redirect('index')


def fetch_comments(request):
    post_id = request.GET.get('id')
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    comments_list = [
        {
            'id': comment.id,
            'body': comment.body,
            'image': comment.image.url if comment.image else '',
            'username': post.user.username,
            'profile_image': post.user.profile.image.url if post.user.profile.image else '',
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for comment in comments
    ]
    return JsonResponse({'status': 'success', 'comments': comments_list, 'total_comments': comments.count()})


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
