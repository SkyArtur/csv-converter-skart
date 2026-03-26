"""Utilities for classifying encoding detection confidence levels."""

from csv_converter.functions.decorator import exception_handling


@exception_handling
def verify_confidence(detection: dict) -> dict[str, float]:
    """Classify a detected encoding confidence score.

    Args:
        detection: Mapping returned by the encoding detector. It must contain
            the ``confidence`` and ``encoding`` keys.

    Returns:
        dict[str, float]: Mapping with the normalized confidence ``value``,
        detected ``encoding``, and a confidence ``tag``.

    Raises:
        ValueError: If required keys are missing or if the confidence value
            cannot be converted by the exception handling decorator.
    """
    value, encoding, tag = float(detection['confidence']), detection['encoding'], ''
    if value >= 0.7:
        tag = 'high'
    elif value >= 0.3:
        tag = 'medium'
    else:
        tag = 'low'
    return {'tag': tag, 'value': value, 'encoding': encoding}
