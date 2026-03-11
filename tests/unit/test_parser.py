from web_valueist.lib.parser import parse, _clean_float_string, _parse_int, _parse_float, _parse_bool

def test_clean_float_string():
    assert _clean_float_string("1,234.56") == "1234.56"
    assert _clean_float_string("1.234,56") == "1234.56"
    assert _clean_float_string("$ 10.50") == "10.50"
    assert _clean_float_string("1.2345") == "1.2345"
    assert _clean_float_string("1,234.567") == "1234.567"
    assert _clean_float_string("1.234.567,89") == "1234567.89"
    assert _clean_float_string("1,234,567.89") == "1234567.89"
    assert _clean_float_string("-10.50") == "-10.50"
    assert _clean_float_string("-$ 10.50") == "-10.50"

def test_parse_int():
    assert _parse_int("100") == 100
    assert _parse_int("100.51") == 101
    assert _parse_int("100.49") == 100

def test_parse_float():
    assert _parse_float("100.50") == 100.5
    assert _parse_float("1,000.75") == 1000.75

def test_parse_bool():
    assert _parse_bool("True") is True
    assert _parse_bool("False") is False
    assert _parse_bool("1") is True
    assert _parse_bool("0") is False
    assert _parse_bool("yes") is True
    assert _parse_bool("no") is False
    assert _parse_bool("Y") is True
    assert _parse_bool("N") is False
    assert _parse_bool("t") is True
    assert _parse_bool("f") is False
    assert _parse_bool("unknown") is False

def test_parse_interface():
    assert parse("int", "10") == 10
    assert parse("float", "10.5") == 10.5
    assert parse("str", "hello") == "hello"
    assert parse("bool", "true") is True
