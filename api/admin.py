from django.contrib import admin
from .models import User, Client

admin.site.register(Client)
admin.site.register(User)