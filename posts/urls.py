from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug>/", views.group_posts),
    path("new/", views.new_post, name="new_post"),
    path("<username>/", views.profile, name="profile"),
    path("<username>/feed/", views.feed, name="feed"),
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit", views.post_edit, name="post_edit"),
    path("stuff/likeprocessor", views.like, name="like_post"),
    path("stuff/dislikeprocessor", views.dislike, name="dislike_post"),
]