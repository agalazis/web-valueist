import pytest
from web_valueist import evaluate, ValueNotFound
import logging

def test_evaluate_float_parser(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100.50</span></body></html>')

    result = evaluate(url, ".price", "float", ">", "100.25")
    assert result["success"] is True
    assert result["value"] == "100.50"

def test_evaluate_ne_operator(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="val">apple</span></body></html>')

    result = evaluate(url, ".val", "str", "ne", "orange")
    assert result["success"] is True

    result = evaluate(url, ".val", "str", "!=", "apple")
    assert result["success"] is False

def test_value_not_found_exception(requests_mock):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body></body></html>')

    with pytest.raises(ValueNotFound):
        evaluate(url, ".non-existent", "str", "eq", "val")

def test_logging_optimization(requests_mock, caplog):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    # Test with DEBUG level
    with caplog.at_level(logging.DEBUG):
        evaluate(url, ".price", "int", ">", "50")

    assert "Found value ['100']" in caplog.text
    # Check that we only have one "Found value" log (plus the "Looking for" one)
    found_value_logs = [record.message for record in caplog.records if "Found value" in record.message]
    assert len(found_value_logs) == 1

    caplog.clear()

    # Test with INFO level (should not log "Found value")
    with caplog.at_level(logging.INFO):
        evaluate(url, ".price", "int", ">", "50")

    assert "Found value ['100']" not in caplog.text
