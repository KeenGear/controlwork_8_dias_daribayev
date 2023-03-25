from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(),
                                related_name='profile',
                                on_delete=models.CASCADE,
                                verbose_name='User profile'
                                )
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pic', verbose_name='avatar')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Birth Date')

    def __str__(self):
        return f'{self.user}'
