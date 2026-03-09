from web_valueist.lib.operator import apply

def test_apply_comparison_operators():
    assert apply("gt", 100, 50) is True
    assert apply(">", 100, 50) is True
    assert apply("lt", 50, 100) is True
    assert apply("<", 50, 100) is True
    assert apply("ge", 100, 100) is True
    assert apply(">=", 100, 50) is True
    assert apply("le", 50, 50) is True
    assert apply("<=", 50, 100) is True

def test_apply_equality_operators():
    assert apply("eq", "apple", "apple") is True
    assert apply("=", "apple", "apple") is True
    assert apply("eq", 100, 100) is True

    assert apply("ne", "apple", "orange") is True
    assert apply("!=", "apple", "apple") is False
    assert apply("ne", 100, 200) is True

def test_apply_with_mixed_types():
    assert apply("gt", 100.5, 100.25) is True
    assert apply("lt", 50.5, 100) is True
    assert apply("eq", 100.0, 100) is True
