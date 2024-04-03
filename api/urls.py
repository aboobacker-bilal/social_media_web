from django.urls import path
from . import views

urlpatterns = [
    path("api_post", views.get_post, name="get-post"),
    path("api_post/<int:pk>/", views.get_post_list, name="post-list"),
]
