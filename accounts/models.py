from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):	
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	profile_photo = models.FileField(upload_to='users/%Y/%m/%d/', blank=True)
	date_of_birth = models.DateField(null=True, blank=True, help_text='Required. Format: YYYY-MM-DD')
	id_number = models.IntegerField(blank=True, null=True, unique=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
	email_confirmed = models.BooleanField(default=False)


#signals
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

	instance.profile.save()		
