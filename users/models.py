from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    class ROLE_CHOICES(models.TextChoices):
        USER = 'user',
        MODERATOR = 'moderator',
        ADMIN = 'admin',

    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES.choices,
                            default=ROLE_CHOICES.USER)
    confirmation_code = models.CharField(max_length=30, default='0000')
    objects = UserManager()
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False
