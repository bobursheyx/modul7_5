from django.contrib import admin
from .models import ORDINARY_USER, User, UserConfirm, Shared
# Register your models here.

admin.site.register(User)
admin.site.register(UserConfirm)
admin.site.register(Shared)