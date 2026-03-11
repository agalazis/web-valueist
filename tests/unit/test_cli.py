import sys
from unittest.mock import patch
from web_valueist.__main__ import _detect_optional_arguments

def test_detect_optional_arguments_with_6_args():
    test_args = ["web_valueist", "http://example.com", "int", "ANY", ".price", ">", "100"]
    with patch.object(sys, 'argv', test_args):
        config = {"quantifier": {"position": 2, "possible_values": ["ANY", "EVERY"]}}
        result = _detect_optional_arguments(config)
        assert result["quantifier"] is True

def test_detect_optional_arguments_with_5_args_and_any_selector():
    # If there are only 5 positional args, the 3rd one (index 2) is the selector.
    # It should NOT be detected as a quantifier even if its value is "ANY".
    test_args = ["web_valueist", "http://example.com", "int", "ANY", ">", "100"]
    with patch.object(sys, 'argv', test_args):
        config = {"quantifier": {"position": 2, "possible_values": ["ANY", "EVERY"]}}
        result = _detect_optional_arguments(config)
        assert result["quantifier"] is False

def test_detect_optional_arguments_with_every_quantifier():
    test_args = ["web_valueist", "http://example.com", "int", "EVERY", ".price", ">", "100"]
    with patch.object(sys, 'argv', test_args):
        config = {"quantifier": {"position": 2, "possible_values": ["ANY", "EVERY"]}}
        result = _detect_optional_arguments(config)
        assert result["quantifier"] is True
