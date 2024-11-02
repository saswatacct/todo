from django.urls import path

from .views import LoginView, LogoutView, SignupView

urlpatterns = [
    path("accounts/login/", LoginView.as_view(), name="account_login"),
    path("accounts/signup/", SignupView.as_view(), name="account_signup"),
    path("accounts/logout/", LogoutView.as_view(), name="account_logout"),
]
