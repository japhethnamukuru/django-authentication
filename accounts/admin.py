from django.contrib import admin
from .models import Profile

@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth', 'profile_photo', 'id_number', 'location', 'date_joined', 'last_login', 'email_confirmed']
