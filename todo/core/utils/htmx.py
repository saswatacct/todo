from collections.abc import Mapping
from typing import Any, NotRequired, Optional, TypedDict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


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
) -> HttpResponse:
    """Render a template and swap the response. Optionally trigger client events.

    Args:
        request (HttpRequest): Request object
        template_name (str): Template name
        params (SwapParams): Swap parameters
        context (Mapping[str, Any], optional): Context data. Defaults to None.

    Raises:
        ValueError: If trigger is invalid

    Returns:
        HttpResponse: Response object
    """

    # Render the template with the context
    # and swap the response with the specified parameters
    return reswap(
        render(
            request,
            template_name,
            context,
        ),
        params,
    )
