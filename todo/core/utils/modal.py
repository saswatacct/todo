from collections.abc import Mapping
from typing import Any

from django.http import HttpRequest, HttpResponse
from django_htmx.http import trigger_client_event

SHOW_MODAL_EVENT = "show-modal"
HIDE_MODAL_EVENT = "hide-modal"


def show_modal(response: HttpResponse, options: Mapping[str, Any]) -> HttpResponse:
    """Show a modal after a request.

    Args:
        response (HttpResponse): The response object.
        options (Mapping[str, Any]): The options to show the modal.

    Returns:
        HttpResponse: The response object.
    """

    return trigger_client_event(response, SHOW_MODAL_EVENT, options)


def hide_modal(response: HttpResponse, options: Mapping[str, Any]) -> HttpResponse:
    """Hide a modal after a request.

    Args:
        response (HttpResponse): The response object.
        options (Mapping[str, Any]): The options to show the modal.

    Returns:
        HttpResponse: The response object.
    """

    return trigger_client_event(response, HIDE_MODAL_EVENT, options)


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
