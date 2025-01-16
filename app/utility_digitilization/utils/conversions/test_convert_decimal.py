from decimal import Decimal
from .convert_decimal import convert_float_to_decimal  # Replace 'your_module' with the actual module path


def test_convert_float_to_decimal_with_list():
    input_data = [
        {"a": Decimal("10.5"), "b": None, "c": "text"},
        {"a": Decimal("5.0"), "b": 15, "c": None},
    ]
    expected_output = [
        {"a": 10.5, "b": 0, "c": "text"},
        {"a": 5.0, "b": 15, "c": 0},
    ]

    result = convert_float_to_decimal(input_data)
    assert result == expected_output


def test_convert_float_to_decimal_with_dict():
    input_data = {
        "a": Decimal("10.5"),
        "b": None,
        "c": "text",
        "d": Decimal("0.0"),
    }
    expected_output = {
        "a": 10.5,
        "b": 0,
        "c": "text",
        "d": 0.0,
    }

    result = convert_float_to_decimal(input_data)
    assert result == expected_output


def test_convert_float_to_decimal_with_empty_list():
    input_data = []
    expected_output = []

    result = convert_float_to_decimal(input_data)
    assert result == expected_output


def test_convert_float_to_decimal_with_empty_dict():
    input_data = {}
    expected_output = {}

    result = convert_float_to_decimal(input_data)
    assert result == expected_output


def test_convert_float_to_decimal_with_invalid_type():
    input_data = "not a list or dict"
    expected_output = "not a list or dict"

    result = convert_float_to_decimal(input_data)
    assert result == expected_output
