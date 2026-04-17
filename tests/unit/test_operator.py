from web_valueist.lib.operator import get_operator

def test_get_operator_comparison_operators():
    assert get_operator("gt")(100, 50) is True
    assert get_operator(">")(100, 50) is True
    assert get_operator("lt")(50, 100) is True
    assert get_operator("<")(50, 100) is True
    assert get_operator("ge")(100, 100) is True
    assert get_operator(">=")(100, 50) is True
    assert get_operator("le")(50, 50) is True
    assert get_operator("<=")(50, 100) is True

def test_get_operator_equality_operators():
    assert get_operator("eq")("apple", "apple") is True
    assert get_operator("=")("apple", "apple") is True
    assert get_operator("eq")(100, 100) is True

    assert get_operator("ne")("apple", "orange") is True
    assert get_operator("!=")("apple", "apple") is False
    assert get_operator("ne")(100, 200) is True

def test_get_operator_with_mixed_types():
    assert get_operator("gt")(100.5, 100.25) is True
    assert get_operator("lt")(50.5, 100) is True
    assert get_operator("eq")(100.0, 100) is True
