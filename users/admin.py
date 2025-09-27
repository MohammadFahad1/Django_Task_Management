from django.contrib import admin
from users.models import CustomUser

# Register your models here.
admin.site.site_header = "Task Management Admin"
admin.site.site_title = "Task Management Admin Portal"
admin.site.index_title = "Welcome to Task Management Admin Portal"
admin.site.register(CustomUser)
