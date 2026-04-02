import os


class StaticCacheControlMiddleware:
    """
    Adds lightweight cache headers for static assets served by Django.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_seconds = int(os.getenv("STATIC_CACHE_SECONDS", "604800"))

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.path.startswith("/static/")
            and response.status_code == 200
            and "Cache-Control" not in response
        ):
            response["Cache-Control"] = f"public, max-age={self.cache_seconds}, immutable"
        return response
