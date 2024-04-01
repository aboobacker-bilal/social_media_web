from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Like, Comment
from .forms import UserPostForm
from user.models import UserProfile

# Create your views here.


def get_post(request):
    posts = Post.objects.all()
    user_likes = []

    if request.user.is_authenticated:
        user_likes = Like.objects.filter(user=request.user,
                                         post__in=posts).values_list(
            'post__id', flat=True)
    context = {
        'posts': posts,
        'user_likes': user_likes,
    }
    return render(request, 'post/post.html', context)


def get_post_list(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'posts': post,
    }
    return render(request, 'post/post.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = request.user.userprofile
            post = form.save(commit=False)
            post.user = user_profile
            form.save()
            return redirect('get-user', pk=request.user.pk)
    else:
        form = UserPostForm()
    context = {
        'forms': form,
    }
    return render(request, 'post/add_post.html', context)


def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        post.delete()
        return redirect('get-user', pk=request.user.pk)
    context = {
        'posts': post
    }
    return render(request, 'post/delete_post.html', context)


def search_user(request):
    if 'q' in request.GET:
        query = request.GET['q']
        results = UserProfile.objects.filter(user__username__icontains=query)
    else:
        results = User.objects.none()
    return render(request, 'post/search_user.html', {'results': results})


def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user
    existing_like = Like.objects.filter(user=user, post=post).exists()
    if existing_like:
        Like.objects.filter(user=user, post=post).delete()
    else:
        Like.objects.create(user=user, post=post)
    return redirect('get-post')


def post_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(user=user, post=post, comment=comment)
            return redirect('get-post')
    return render(request, 'post/post.html', {'post': post})

