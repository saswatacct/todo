from allauth.account.views import LoginView, SignupView
from django.urls import path

from .views import CustomLogoutView

urlpatterns = [
    path("accounts/login/", LoginView.as_view(), name="account_login"),
    path("accounts/signup/", SignupView.as_view(), name="account_signup"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="account_logout"),
]
