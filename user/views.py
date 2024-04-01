from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Follow
from .forms import UserProfileForm, LoginForm

from django.contrib.auth.forms import UserCreationForm

from post.models import Post
from post.forms import UserPostForm

# Create your views here.


def user_login(request):
    form = LoginForm
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('get-post')
            else:
                message = 'Login Failed'
    context = {
        'form': form,
        'message': message
    }
    return render(request, 'user/user_login.html', context)


def user_logout(request):
    logout(request)
    return redirect('user-login')


def user_sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('user-login')
    else:
        form = UserCreationForm()
    context = {
        'forms': form
    }
    return render(request, 'user/user_sign_up.html', context)


@login_required
def get_user_profile(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    is_following = Follow.objects.filter(followers=request.user,
                                         following=user.user)
    followers_count = Follow.objects.filter(following=user.user).count()
    following_count = Follow.objects.filter(followers=user.user).count()
    context = {
        'users': user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'user/user_profile.html', context)


@login_required
def edit_user_profile(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    form = UserProfileForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('get-user', pk=user_id)
    context = {
        'forms': form,
    }
    return render(request, 'user/profile_edit.html', context)


def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'posts': post,
    }
    return render(request, 'user/single_post.html', context)


def user_follow(request, pk):
    follow = User.objects.get(pk=pk)
    is_following = Follow.objects.filter(followers=request.user,
                                         following=follow).exists()

    if is_following:
        Follow.objects.filter(followers=request.user,
                              following=follow).delete()
    else:
        follow = Follow(followers=request.user, following=follow)
        follow.save()

    return redirect('get-user', pk=pk)
