from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserLoginView.as_view(), name="user-login"),
    path("logout", views.UserLogOutView.as_view(), name='logout'),
    path("sign_up", views.UserSignUp.as_view(), name="sign-up"),
    path("user/<int:pk>/", views.UserProfileView.as_view(), name="get-user"),
    path("edit_pro/<int:pk>", views.EditUserProfile.as_view(),
         name="edit-profile"),
    path("post_view/<int:pk>/", views.PostView.as_view(), name="view-post"),
    path("follow/<int:pk>/", views.UserFollowView.as_view(), name="follow"),
]
