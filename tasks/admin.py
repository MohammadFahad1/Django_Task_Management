from django.contrib import admin

# Register your models here.
from tasks.models import Tasks, TaskDetail, Project, Employee

admin.site.register(Tasks)
admin.site.register(TaskDetail)
admin.site.register(Project)
admin.site.register(Employee)