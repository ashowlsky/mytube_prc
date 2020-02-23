from users.models import Relations, User
from posts.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    """ Отправляет сообщение всем подписчикам пользователя при создании нового поста. Работает также, как и функция feed"""
    if created:
        user = instance.author
        id_pool = [relation.follower_id for relation in user.followed.all()]
        followers = [User.objects.get(id=i) for i in id_pool]
        email_pool = [user.email for user in followers]
        send_mail(
            'New post!', f'{user.first_name} {user.last_name} posted something, check it out!', 'user_notifier@mytube.com', email_pool
        )

