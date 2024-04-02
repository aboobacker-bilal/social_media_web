from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import UserProfile, Follow
from .forms import UserProfileForm, LoginForm
from django.contrib.auth.forms import UserCreationForm

from post.models import Post
# Create your views here.


class UserLoginView(LoginRequiredMixin, View):
    def get(self, request):
        form = LoginForm
        message = ''
        context = {
            'form': form,
            'message': message
        }
        return render(request, 'user/user_login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('get-post')
        context = {
            'form': form,
            'message': 'Login failed!'
        }
        return render(request, 'user/user_login.html', context)


class UserLogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('user-login')


class UserSignUp(View):
    def get(self, request):
        form = UserCreationForm
        context = {
            'forms': form
        }
        return render(request, 'user/user_sign_up.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')

        context = {
            'forms': form
        }
        return render(request, 'user/user_sign_up.html', context)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(UserProfile, pk=pk)
        is_following = Follow.objects.filter(followers=request.user,
                                             following=user.user)
        followers_count = Follow.objects.filter(following=user.user).count()
        following_count = Follow.objects.filter(followers=user.user).count()
        post_count = Post.objects.filter(user=user).count()
        context = {
            'users': user,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'post_count': post_count,
        }
        return render(request, 'user/user_profile.html', context)


class EditUserProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('get-user', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'posts': post,
        }
        return render(request, 'user/single_post.html', context)


class UserFollowView(LoginRequiredMixin, View):
    def post(self, request, pk):
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
