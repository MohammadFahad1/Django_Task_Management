from django.urls import path
from users.views import admin_dashboard, create_group, sign_in, sign_out, sign_up, activate_user, assign_role

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('sign-out/', sign_out, name="logout"),
    path('activate/<int:user_id>/<str:token>/', activate_user, name="activate-user"),
    path('admin/dashboard', admin_dashboard, name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name='create-group')
]
