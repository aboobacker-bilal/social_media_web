from django.urls import path
from . import views

urlpatterns = [
    path("post", views.get_post, name="get-post"),
    path("post/<int:pk>/", views.get_post_list, name="post-list"),
    path("add_post", views.add_post, name='add-post'),
    path("delete_post/<int:pk>/", views.delete_post, name="delete-post"),
    path("search_user", views.search_user, name="search-user"),
    path("like/<int:pk>/", views.post_like, name="post-like"),
    path("comments/<int:pk>/", views.post_comments, name="comments"),
]
