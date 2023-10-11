from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# i am not going to use this at all i will remove this in final PR
@receiver(post_save, sender=User)
def generate_auto_username(sender, instance, **kwargs):
    if not instance.username:
        username = f'{instance.first_name}_{instance.last_name}'.lower()
        cnt = 1
        while User.objects.filter(username=username):
            username = f'{instance.first_name}_{instance.last_name}_{cnt}'.lower()
            cnt += 1
        instance.username = username