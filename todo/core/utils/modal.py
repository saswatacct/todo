from collections.abc import Mapping
from functools import wraps
from typing import Any, Callable, Optional

from django.http import HttpResponse
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
        view (Callable[..., HttpResponse]): The view function.

    Returns:
        Callable[..., HttpResponse]: The wrapper function.
    """

    @wraps(view)
    def wrapper(*args, **kwargs) -> HttpResponse:
        response = view(*args, **kwargs)
        return trigger_client_event(response, HIDE_MODAL_EVENT)

    return wrapper
