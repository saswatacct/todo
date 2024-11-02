from allauth.account.views import LoginView as BaseLoginView
from allauth.account.views import LogoutView as BaseLogoutView
from allauth.account.views import SignupView as BaseSignupView
from django.http import HttpResponse
from django.urls import reverse

from todo.core.mixins import ModalMixin, SuccessRedirectMixin


class LogoutView(ModalMixin, BaseLogoutView):
    """Custom logout view that redirects to the login page using htmx."""

    # Because the logout view is a post request, we need to handle the post request
    # by hand (without using the SuccessRedirectMixin) to redirect to the login page
    # using htmx.
    def post(self, *args, **kwargs) -> HttpResponse:
        """
        Handle the post request. Redirect to the login page using htmx.
        """

        response = super().post(*args, **kwargs)
        response.status_code = 200
        response.headers["HX-Location"] = reverse("account_login")
        return response


class LoginView(SuccessRedirectMixin, BaseLoginView):
    """Custom login view that redirects to the home page using htmx."""

    success_url = "/"


class SignupView(SuccessRedirectMixin, BaseSignupView):
    """Custom login view that redirects to the home page using htmx."""

    success_url = "/"
