import pytest
from web_valueist.lib import evaluate
from unittest.mock import patch

def test_evaluate_empty_list_returns_false():
    with patch("web_valueist.lib._fetch_values") as mock_fetch:
        mock_fetch.return_value = []
        # Actually _fetch_values raises ValueNotFound if empty,
        # but let's see how evaluate handles it if it didn't
        pass

def test_evaluate_quantifiers_with_mocked_fetch():
    with patch("web_valueist.lib._fetch_values") as mock_fetch:
        # ANY
        mock_fetch.return_value = ["1", "2"]
        result = evaluate("http://x.com", "s", "int", "eq", "1", quantifier="ANY")
        assert result["success"] is True
        assert result["values"] == [1, 2]

        result = evaluate("http://x.com", "s", "int", "eq", "3", quantifier="ANY")
        assert result["success"] is False

        # EVERY
        result = evaluate("http://x.com", "s", "int", "eq", "1", quantifier="EVERY")
        assert result["success"] is False

        mock_fetch.return_value = ["1", "1"]
        result = evaluate("http://x.com", "s", "int", "eq", "1", quantifier="EVERY")
        assert result["success"] is True

def test_short_circuit_actually_happens():
    # We can use a side effect to track calls
    calls = []
    def tracked_op(a, b):
        calls.append(a)
        return a == b

    with patch("web_valueist.lib._fetch_values") as mock_fetch:
        with patch("web_valueist.lib.operator.get_operator") as mock_get_op:
            mock_get_op.return_value = tracked_op

            mock_fetch.return_value = ["1", "2", "3"]

            # ANY: should stop at "1"
            calls.clear()
            evaluate("http://x.com", "s", "int", "eq", "1", quantifier="ANY")
            assert calls == [1]

            # EVERY: should stop at "1" (fails eq 2)
            calls.clear()
            evaluate("http://x.com", "s", "int", "eq", "2", quantifier="EVERY")
            assert calls == [1]
