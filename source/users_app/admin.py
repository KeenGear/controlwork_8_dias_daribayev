from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('birth_date', 'avatar')


class ProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)


User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)
