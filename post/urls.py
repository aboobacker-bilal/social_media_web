from django.urls import path
from . import views

urlpatterns = [
    path("post", views.GetPostView.as_view(), name="get-post"),
    path("post/<int:pk>/", views.GetPostListView.as_view(), name="post-list"),
    path("add_post", views.CreatePostView.as_view(), name='add-post'),
    path("delete_post/<int:pk>/", views.DeletePostView.as_view(),
         name="delete-post"),
    path("search_user", views.UserSearchListView.as_view(), name="search-user"),
    path("like/<int:pk>/", views.PostLikeView.as_view(), name="post-like"),
    path("comments/<int:pk>/", views.PostCommentsView.as_view(),
         name="comments"),
]
