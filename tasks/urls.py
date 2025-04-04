from django.urls import path
from tasks.views import create_task, dashboard, manager_dashboard, task_details, user_dashboard, test, view_task, update_task, delete_task

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('test', test),
    path('create-task', create_task, name='create-task'),
    path('view-task', view_task),
    path('task/<int:task_id>/details/', task_details, name="task-details"),
    path('update-task/<int:id>/', update_task, name='update-task'),
    path('delete-task/<int:id>/', delete_task, name='delete-task'),
    path('dashboard/', dashboard, name='dashboard'),
]