from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Post,Comment,Room,Message

# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(Message)