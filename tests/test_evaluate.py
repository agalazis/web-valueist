import pytest
from web_valueist import evaluate, ValueNotFound

def test_evaluate_any_quantifier_returns_true_if_at_least_one_match_satisfies_condition(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='''
        <html><body>
            <span class="price">100</span>
            <span class="price">200</span>
        </body></html>
    ''')

    # ANY > 150 should be true because 200 > 150
    result = evaluate(url, ".price", "int", ">", "150", quantifier="ANY")
    assert result["success"] is True
    assert result["value"] == ["100", "200"]

def test_evaluate_every_quantifier_returns_false_if_any_match_fails_condition(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='''
        <html><body>
            <span class="price">100</span>
            <span class="price">200</span>
        </body></html>
    ''')

    # EVERY > 150 should be false because 100 <= 150
    result = evaluate(url, ".price", "int", ">", "150", quantifier="EVERY")
    assert result["success"] is False

def test_evaluate_every_quantifier_returns_true_if_all_matches_satisfy_condition(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='''
        <html><body>
            <span class="price">100</span>
            <span class="price">200</span>
        </body></html>
    ''')

    # EVERY > 50 should be true
    result = evaluate(url, ".price", "int", ">", "50", quantifier="EVERY")
    assert result["success"] is True

def test_evaluate_default_quantifier_is_any(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='''
        <html><body>
            <span class="price">100</span>
            <span class="price">200</span>
        </body></html>
    ''')

    result = evaluate(url, ".price", "int", ">", "150")
    assert result["success"] is True

def test_evaluate_returns_dictionary_with_success_and_value(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    result = evaluate(url, ".price", "int", ">", "50")

    assert isinstance(result, dict)
    assert result["success"] is True
    assert result["value"] == "100"

def test_evaluate_with_float_parser(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100.50</span></body></html>')

    result = evaluate(url, ".price", "float", ">", "100.25")
    assert result["success"] is True
    assert result["value"] == "100.50"

def test_evaluate_with_not_equal_operators(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="val">apple</span></body></html>')

    result = evaluate(url, ".val", "str", "ne", "orange")
    assert result["success"] is True

    result = evaluate(url, ".val", "str", "!=", "apple")
    assert result["success"] is False

def test_evaluate_raises_value_not_found_when_selector_matches_nothing(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body></body></html>')

    with pytest.raises(ValueNotFound):
        evaluate(url, ".non-existent", "str", "eq", "val")
