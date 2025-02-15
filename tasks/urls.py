from django.urls import path
from tasks.views import create_task, manager_dashboard, user_dashboard, test, view_task

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('user-dashboard/', user_dashboard),
    path('test', test),
    path('create-task', create_task),
    path('view-task', view_task)
]