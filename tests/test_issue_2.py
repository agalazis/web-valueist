import pytest
from web_valueist import evaluate
import logging

def test_evaluate_any_quantifier(requests_mock):
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

def test_evaluate_every_quantifier(requests_mock):
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

    # EVERY > 50 should be true
    result = evaluate(url, ".price", "int", ">", "50", quantifier="EVERY")
    assert result["success"] is True

def test_evaluate_default_is_any(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='''
        <html><body>
            <span class="price">100</span>
            <span class="price">200</span>
        </body></html>
    ''')

    result = evaluate(url, ".price", "int", ">", "150")
    assert result["success"] is True
