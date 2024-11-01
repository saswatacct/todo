from typing import Callable
from urllib.parse import urlparse

from django.http import HttpRequest, HttpResponse
from django.urls import resolve


def authentication_redirect_middlware(get_response: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)

        if request.htmx:
            # Get full url from headers
            location = request.headers.get("HX-Current-URL")

            # If no location, return response
            if not location:
                return response

            # Parse the location
            parsed = urlparse(location)

            # Resolve the name of the view
            name = resolve(parsed.path).url_name

            # If the view has the name "account_*", redirect to the home page
            if name.startswith("account_") and request.user.is_authenticated:
                response["HX-Redirect"] = "/"

        return response

    return middleware
