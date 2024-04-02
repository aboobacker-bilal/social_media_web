from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_delete, sender=UserProfile)
def delete_user_with_profile(sender, instance, **kwargs):
    if instance.user:
        pre_delete.disconnect(delete_user_with_profile, sender=UserProfile)
        instance.user.delete()
        pre_delete.connect(delete_user_with_profile, sender=UserProfile)
