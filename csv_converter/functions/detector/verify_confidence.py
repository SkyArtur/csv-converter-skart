"""Helpers for classifying encoding detection confidence."""

from csv_converter.functions.decorator import exception_handling


@exception_handling
def verify_confidence(detection: dict) -> dict[str, float]:
    """Classify the confidence level of an encoding detection result.

    Args:
        detection: Mapping returned by the encoding detector. Expected keys are
            ``confidence`` and ``encoding``.

    Returns:
        dict[str, float]: Mapping with the detected ``encoding``, numeric
            confidence ``value``, and confidence ``tag``.

    Raises:
        ValueError: If required keys are missing or the confidence value cannot
            be converted.
    """
    value, encoding, tag = float(detection['confidence']), detection['encoding'], ''
    if value >= 0.7:
        tag = 'high'
    elif value >= 0.3:
        tag = 'medium'
    else:
        tag = 'low'
    return {'tag': tag, 'value': value, 'encoding': encoding}
