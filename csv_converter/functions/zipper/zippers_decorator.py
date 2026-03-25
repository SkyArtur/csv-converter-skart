"""Decorator utilities for ZIP-based helper functions."""

import zipfile
from functools import wraps
from typing import Callable


def zippers_decorator(func: Callable) -> Callable:
    """Wrap a ZIP helper function and normalize common exceptions.

    Args:
        func: Function that performs a ZIP-related file operation.

    Returns:
        Callable: Wrapped function that raises ``ValueError`` for expected
            ZIP and filesystem errors.

    Raises:
        ValueError: If the wrapped function raises ``PermissionError``,
            ``FileNotFoundError``, ``zipfile.BadZipFile``, or ``TypeError``.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Execute the wrapped function with standardized error handling."""
        try:
            return func(*args, **kwargs)
        except (PermissionError, FileNotFoundError, zipfile.BadZipFile, TypeError) as error:
            raise ValueError(f'<func: {func.__name__}> has raised an error.\n{error}')
    return wrapper
