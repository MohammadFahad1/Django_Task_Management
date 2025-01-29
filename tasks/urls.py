from django.urls import path
from tasks.views import show_task, home, contact

urlpatterns = [
    path('', home),
    path('contact/', contact),
    path('show-task', show_task)
]