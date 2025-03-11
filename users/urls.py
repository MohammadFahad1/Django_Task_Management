
from django.urls import path
from users.views import login, sign_up

urlpatterns = [
    path('sign-up', sign_up, name="sign-up"),
    path('sign-in', login, name="sign-in")
]
