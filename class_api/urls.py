from django.urls import path
from . import views

urlpatterns = [
    path("post_api", views.GetPostView.as_view(), name="get-post"),
    path("post_api/<int:pk>/", views.GetPostListView.as_view(),
         name="post-list"),
]