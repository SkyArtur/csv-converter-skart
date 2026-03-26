
"""Decorators for normalizing exceptions raised by helper functions."""

import zipfile
from functools import wraps
from typing import Callable


def exception_handling(func: Callable) -> Callable:
    """Wrap a callable and convert common runtime errors to ``ValueError``.

    Args:
        func: Callable to wrap.

    Returns:
        Callable: Wrapped callable that re-raises selected exceptions as
        ``ValueError``.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Execute the wrapped callable with normalized error handling.

        Args:
            *args: Positional arguments forwarded to ``func``.
            **kwargs: Keyword arguments forwarded to ``func``.

        Returns:
            Any: Value returned by ``func``.

        Raises:
            ValueError: If ``func`` raises one of the handled exceptions.
        """
        try:
            return func(*args, **kwargs)
        except (PermissionError, FileNotFoundError, zipfile.BadZipFile, TypeError, AttributeError, KeyError):
            raise
    return wrapper
