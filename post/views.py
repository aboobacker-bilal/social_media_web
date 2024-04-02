from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from django.urls import reverse_lazy

from .models import Post, Like, Comment
from .forms import UserPostForm
from user.models import UserProfile

# Create your views here.


class GetPostView(View):
    def get(self, request):
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


class GetPostListView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        context = {
            'posts': post,
        }
        return render(request, 'post/post.html', context)


class CreatePostView(CreateView, LoginRequiredMixin):
    model = UserProfile
    form_class = UserPostForm
    template_name = 'post/add_post.html'
    login_url = ''

    def get_success_url(self):
        return reverse_lazy('get-user', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        user_profile = self.request.user.userprofile
        form.instance.user = user_profile
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/delete_post.html'

    def get_success_url(self):
        return reverse_lazy('get-user', kwargs={'pk': self.request.user.pk})


class UserSearchListView(ListView):
    model = UserProfile
    template_name = 'post/search_user.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return UserProfile.objects.filter(user__username__icontains=query)
        else:
            return User.objects.none()


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        user = request.user
        existing_like = Like.objects.filter(user=user, post=post).exists()
        if existing_like:
            Like.objects.filter(user=user, post=post).delete()
        else:
            Like.objects.create(user=user, post=post)
        return redirect('get-post')


class PostCommentsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'post/post.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(user=user, post=post, comment=comment)
            return redirect('get-post')
        return render(request, 'post/post.html', {'post': post})
