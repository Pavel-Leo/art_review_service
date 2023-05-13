from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year: int) -> None:
    """
    Validates that the given year is not in the future.

    :param value: the year to validate
    :raises: ValidationError if the year is in the future
    """

    if year > timezone.now().year:
        raise ValidationError(
            (f"Год не может быть {year} больше текущего!"),
            params={"value": year},
        )
