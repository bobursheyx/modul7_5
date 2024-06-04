from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

# Create your models here.

ORDINARY_USER, ADMIN, MANAGER = ('ordinary_user',  'admin', 'manager')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, CONFIRM, DONE, PHOTO = ('new', 'confirm', 'done', 'done_photo')


class User(AbstractUser):
    USER_TYPES = (
        (ORDINARY_USER, 'Ordinary User'),
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager')
    )
    user_roll = models.CharField(max_length=40, choices=USER_TYPES, default=ORDINARY_USER)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.username


class UserConfirm(models.Model):
    CONFIRM_TYPES = (
        (VIA_EMAIL, 'Email'),
        (VIA_PHONE, 'Phone')
    )
    STATUS_TYPES = (
        (NEW, 'New'),
        (CONFIRM, 'Confirmed'),
        (DONE, 'Done'),
        (PHOTO, 'Photo Done')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    confirm_type = models.CharField(max_length=20, choices=CONFIRM_TYPES, default=VIA_EMAIL)
    confirmation_code = models.CharField(max_length=64, default=get_random_string)
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_confirm_type_display()}'


class Shared(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} shared on {self.created_at}'