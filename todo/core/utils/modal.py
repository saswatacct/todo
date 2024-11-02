from collections.abc import Mapping
from functools import wraps
from typing import Any, Callable, Optional

from django.http import HttpRequest, HttpResponse
from django_htmx.http import trigger_client_event

SHOW_MODAL_EVENT = "show-modal"
HIDE_MODAL_EVENT = "hide-modal"


def show_modal(response: HttpResponse, options: Optional[Mapping[str, Any]] = None) -> HttpResponse:
    """Show a modal after a request.

    Args:
        response (HttpResponse): The response object.
        options (Mapping[str, Any], optional): The options to show the modal. Defaults to None.

    Returns:
        HttpResponse: The response object.
    """

    return trigger_client_event(response, SHOW_MODAL_EVENT, options)


def hide_modal(view: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """Hide a modal after a request.

    Args:
        func (Callable[..., HttpResponse]): The view function.

    Returns:
        Callable[..., HttpResponse]: The wrapper function.
    """

    @wraps(view)
    def wrapper(*args, **kwargs) -> HttpResponse:
        response = view(*args, **kwargs)
        return trigger_client_event(response, HIDE_MODAL_EVENT)

    return wrapper


class ModalMixin:
    """A mixin to show a modal after a HTMX request."""

    modal_options: Mapping[str, Any] = {}

    def get_modal_options(self) -> Mapping[str, Any]:
        """Get the options to show the modal.

        Returns:
            Mapping[str, Any]: The options to show the modal.
        """

        return self.modal_options

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response: HttpResponse = super().get(request, *args, **kwargs)

        if request.htmx:
            response = show_modal(response, self.get_modal_options())

        return response
