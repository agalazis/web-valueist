import pytest
from web_valueist import evaluate
import logging

def test_evaluate_returns_dict(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    result = evaluate(url, ".price", "int", ">", "50")

    assert isinstance(result, dict)
    assert result["success"] is True
    assert result["value"] == "100"

def test_evaluate_logs_value(requests_mock, caplog):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    with caplog.at_level(logging.INFO):
        evaluate(url, ".price", "int", ">", "50")

    assert "Found value ['100']" in caplog.text
