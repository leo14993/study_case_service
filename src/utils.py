import sys
from typing import Tuple
from decimal import Decimal
from datetime import datetime, timezone, timedelta


def get_default_tzinfo() -> timezone:
    return timezone(timedelta(hours=-3))


def get_exception_infos() -> Tuple[str, int]:
    _, _, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno
    return filename, line_number


def convert_datetime_for_schemas(dt: datetime) -> str:
    return str(dt.astimezone())


def get_america_datetime() -> datetime:
    AMERICA_SAO_PAULO = get_default_tzinfo()
    return datetime.now(AMERICA_SAO_PAULO)


def number_format(value, decimal_separator=',', mille_separator='.', significance=2):
    """Format a integer or decimal number like PHP number_format function.
    Args:
        value: The value to be formatted. If its not a valid number, ValueError
            will be rised
        decimal_separator: The string to use to split decimal places
        mille_separator: If specified, milles will be splitted with this string
        significance: Number of decimal places
    Returns:
        A string with the value formatted
    Raises:
        ValueError: If `value` is not a valid number
    """
    if value is None:
        value = 0.0

    if not type(value) in [int, float, Decimal]:
        try:
            value = float(value)
        except ValueError:
            raise ValueError('%s is not a number' % value)

    # convert to string
    format_string = '.%df' % significance
    value = format(value, format_string)

    # split decimal part
    integer, decimal = value.split('.')

    if mille_separator:
        final_value = []
        # add mille_separator to integer part (reverse integer part slicing string)
        count = 0
        for number in integer[::-1]:
            if count > 0 and count % 3 == 0:
                final_value.append(mille_separator)
            final_value.append(number)
            count += 1
        final_value = ''.join(reversed(final_value))
    else:
        final_value = integer

    return '%s%s%s' % (final_value, decimal_separator, decimal)