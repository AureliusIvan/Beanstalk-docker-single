from decimal import Decimal
from typing import Union, List, Dict


def convert_float_to_decimal(data_list: Union[List, Dict]) -> Union[List, Dict]:
    """
    Converts Decimal values in a list or dictionary to float values and converts None (null) values to 0.
    :param data_list: A list or dictionary potentially containing Decimal values or None.
    :return: A modified list or dictionary with Decimal values converted to float and None converted to 0.
    """
    if isinstance(data_list, (list, dict)):
        if isinstance(data_list, list):
            return [
                {k: 0 if v is None else float(v) if isinstance(v, Decimal) else v for k, v in item.items()}
                for item in data_list
            ]
        return {k: 0 if v is None else float(v) if isinstance(v, Decimal) else v for k, v in data_list.items()}
    return data_list
