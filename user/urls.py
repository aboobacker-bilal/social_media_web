from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="user-login"),
    path("logout", views.user_logout, name='logout'),
    path("sign_up", views.user_sign_up, name="sign-up"),
    path("post_view/<int:pk>/", views.view_post, name="view-post"),
    path("user/<int:pk>/", views.get_user_profile, name="get-user"),
    path("edit_pro/<int:user_id>", views.edit_user_profile,
         name="edit-profile"),
    path("follow/<int:pk>/", views.user_follow, name="follow"),
]
