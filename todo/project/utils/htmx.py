from collections.abc import Mapping
from typing import Any, List, NotRequired, Optional, TypedDict, Union

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_htmx.http import trigger_client_event


class SwapParams(TypedDict):
    swap: NotRequired[str]
    target: NotRequired[str]
    select: NotRequired[str]


def reswap(response: HttpResponse, params: SwapParams) -> HttpResponse:
    """Method allows you to specify how the response will be swapped.

    Args:
        response (HttpResponse): Response object
        params (SwapParams): Swap parameters

    Returns:
        HttpResponse: Updated response object
    """

    for key, value in params.items():
        response.headers.setdefault(f"HX-Re{key}", value)

    return response


def render_swap(
    request: HttpRequest,
    template_name: str,
    params: SwapParams,
    context: Optional[Mapping[str, Any]] = None,
    trigger: Optional[Union[List[str], Mapping[str, Any]]] = None,
) -> HttpResponse:
    """Render a template and swap the response. Optionally trigger client events.

    Args:
        request (HttpRequest): Request object
        template_name (str): Template name
        params (SwapParams): Swap parameters
        context (Mapping[str, Any], optional): Context data. Defaults to None.
        trigger (Union[List[str], Mapping[str, Any], optional): Client events. Defaults

    Raises:
        ValueError: If trigger is invalid

    Returns:
        HttpResponse: Response object
    """

    # Render the template
    response = reswap(render(request, template_name, context), params)

    # Trigger client events
    # a bit of spaghetti code
    if trigger:
        # If trigger is a list of events
        if isinstance(trigger, list):
            # Trigger each event
            for event in trigger:
                response = trigger_client_event(response, event)
        # If trigger is a dict of events
        elif isinstance(trigger, dict):
            # Trigger each event with data
            for event, data in trigger.items():
                response = trigger_client_event(response, event, data)
        else:
            raise ValueError("Invalid trigger type")

    # Return the response
    return response
