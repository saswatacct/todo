from allauth.account.views import LoginView, LogoutView, SignupView
from django.contrib import admin
from django.urls import include, path

# Base urls
urlpatterns = [
    path("admin/", admin.site.urls),
]

# Authentication urls
urlpatterns += [
    path("accounts/login/", LoginView.as_view(), name="account_login"),
    path("accounts/signup/", SignupView.as_view(), name="account_signup"),
    path("accounts/logout/", LogoutView.as_view(), name="account_logout"),
]

# App urls
urlpatterns += [
    path("", include("todo.tasks.urls")),
]
