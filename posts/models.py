from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(unique = True)
    description = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="dislikes", blank=True)
    is_new = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text
 
class Comment(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text
