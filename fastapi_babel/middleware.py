from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.base import DispatchFunction
from starlette.types import ASGIApp
from typing import TYPE_CHECKING
from babel.core import Locale

if TYPE_CHECKING:
    from .core import Babel


class InternationalizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, babel: "Babel", dispatch: DispatchFunction = None
    ) -> None:
        super().__init__(app, dispatch)
        self.babel: "Babel" = babel

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        lang_code: str = request.headers.get("Accept-Language", None)
        if lang_code:
            if lang_code not in self.babel.config.ACCEPTABLE_LANGUAGES:
                try:
                    lang_code = Locale.parse(lang_code.split(";")[0], sep='-').language
                except:
                    lang_code = self.babel.config.BABEL_DEFAULT_LOCALE
                if lang_code not in self.babel.config.ACCEPTABLE_LANGUAGES:
                    lang_code = self.babel.config.BABEL_DEFAULT_LOCALE
            self.babel.locale = lang_code
        response = await call_next(request)
        return response
