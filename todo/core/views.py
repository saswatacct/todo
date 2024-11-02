from allauth.account.views import LogoutView
from django.http import HttpResponse

from todo.core.utils.modal import ModalMixin


class CustomLogoutView(ModalMixin, LogoutView):
    """Custom logout view that redirects to the login page using htmx."""

    def post(self, *args, **kwargs) -> HttpResponse:
        """
        Handle the post request. Redirect to the login page using htmx.
        """

        response = super().post(*args, **kwargs)
        response.status_code = 200
        response.headers["HX-Redirect"] = "/accounts/login/"
        return response
