import logging
from web_valueist import evaluate

def test_evaluate_logs_found_values_in_debug_mode(requests_mock, caplog):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    with caplog.at_level(logging.DEBUG):
        evaluate(url, ".price", "int", ">", "50")

    assert "Found value ['100']" in caplog.text

def test_logging_is_optimized_and_not_redundant(requests_mock, caplog):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    # Test with DEBUG level
    with caplog.at_level(logging.DEBUG):
        evaluate(url, ".price", "int", ">", "50")

    assert "Found value ['100']" in caplog.text
    # Check that we only have one "Found value" log
    found_value_logs = [record.message for record in caplog.records if "Found value" in record.message]
    assert len(found_value_logs) == 1

def test_no_expensive_logs_produced_at_info_level(requests_mock, caplog):
    url = "https://example.com"
    requests_mock.get(url, text='<html><body><span class="price">100</span></body></html>')

    # Test with INFO level (should not log "Found value" or "Looking for")
    with caplog.at_level(logging.INFO):
        evaluate(url, ".price", "int", ">", "50")

    assert "Found value ['100']" not in caplog.text
    assert "Looking for" not in caplog.text
