
from django.urls import path
from users.views import sign_in, sign_up

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in")
]
