from django.urls import path
from tasks.views import CreateTask, ManagerDashboard, TaskDetail, UpdateTask, dashboard, ManagerDashboard, UserDashboard, DeleteTask, Greetings, HiGreetings, HelloGreetings, ViewProject, UpdateTask

urlpatterns = [
    path('manager-dashboard/', ManagerDashboard.as_view(), name='manager-dashboard'),
    path('user-dashboard/', UserDashboard.as_view(), name='user-dashboard'),
    path('create-task', CreateTask.as_view(), name='create-task'),
    path('task/<int:task_id>/details/', TaskDetail.as_view(), name="task-details"),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    path('delete-task/<int:id>/', DeleteTask.as_view(), name='delete-task'),
    path('dashboard/', dashboard, name='dashboard'),
    path('greetings/', HelloGreetings.as_view(greetings="Hello bhaiya kemon achen ?"), name="greetings"),
]