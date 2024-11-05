from django.http import HttpRequest, HttpResponse

from todo.core.utils.modal import show_modal


class ModalMixin:
    """A mixin to show a modal after a HTMX request."""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().get(request, *args, **kwargs)

        if request.htmx:
            response = show_modal(response)

        return response


class SuccessRedirectMixin:
    """A mixin to redirect after a successful form submission."""

    def form_valid(self, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().form_valid(*args, **kwargs)
        response["HX-Redirect"] = self.get_success_url()
        # Set the status code to 200 to force HTMX to
        # follow the redirect.
        response.status_code = 200
        return response
