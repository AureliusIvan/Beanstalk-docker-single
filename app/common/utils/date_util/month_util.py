import calendar


def int_to_month_name(month: int) -> str:
    """
    Convert int to month name (e.g. 1 -> January)
    :param month:
    :return:
    """
    return calendar.month_name[month]
