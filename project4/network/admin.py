from django.contrib import admin

from .models import User, Comments, Post
# Register your models here.

admin.site.register(User),
admin.site.register(Comments),
admin.site.register(Post)