from django import template
from django.urls import path
from users.views import AssignRoleView, CustomLoginView, CustomPasswordResetView, EditProfileView, AdminDashboardView, CreateGroupView, GroupListView, sign_in, sign_out, sign_up, activate_user, ProfileView, ChangePassword, CustomPasswordResetConfirmView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView
# from django.views.generic import TemplateView

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', CustomLoginView.as_view(), name="sign-in"),
    path('sign-out/', LogoutView.as_view(), name="logout"),
    path('activate/<int:user_id>/<str:token>/', activate_user, name="activate-user"),
    path('admin/dashboard', AdminDashboardView.as_view(), name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', AssignRoleView.as_view(), name="assign-role"),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    path('admin/group-list/', GroupListView.as_view(), name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', ChangePassword.as_view(), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
]