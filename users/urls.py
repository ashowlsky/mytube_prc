from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("manageuserprofile/", views.manage_user_profile, name="manageuserprofile"),
    path("followingprocessor/", views.follow, name="followuser"),
    path("unfollowingprocessor/", views.unfollow, name='unfollowuser'),
]