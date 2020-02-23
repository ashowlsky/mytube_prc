from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatars')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.avatar.path)
        
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

class Relations(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    started_on = models.DateField(auto_now_add=True)

class Logout_time_records(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logout_time")
    last_logout_time = models.DateTimeField(blank=True, null=True)

# Create your models here.
