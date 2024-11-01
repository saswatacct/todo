from allauth.account.views import LogoutView

from todo.core.utils.modal import ModalMixin


class CustomLogoutView(ModalMixin, LogoutView):
    """Custom logout view that redirects to the login page using htmx."""

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        response.status_code = 200
        response.headers["HX-Redirect"] = "/accounts/login/"
        return response
