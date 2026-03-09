import subprocess
import json
import pytest
import sys

def test_cli_quantifier_disambiguation():
    # Selector is 'ANY', no quantifier specified.
    # Positions: url parser selector operator value
    # http://example.com str ANY eq "val" -> 5 positional args
    # The CLI should NOT detect 'ANY' as a quantifier because there are only 5 positional args.

    cmd = [
        sys.executable, "-m", "web_valueist",
        "http://example.com", "str", "h1", "eq", "Example Domain", "--json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, env={"PYTHONPATH": "."})
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["args"]["quantifier"] == "ANY"
    assert data["args"]["selector"] == "h1"

def test_cli_with_actual_quantifier():
    # Positions: url parser quantifier selector operator value -> 6 args
    cmd = [
        sys.executable, "-m", "web_valueist",
        "http://example.com", "str", "EVERY", "h1", "eq", "Example Domain", "--json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, env={"PYTHONPATH": "."})
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["args"]["quantifier"] == "EVERY"
    assert data["args"]["selector"] == "h1"

def test_cli_selector_named_any():
    # Positions: url parser selector operator value -> 5 args
    # Selector is 'ANY'
    cmd = [
        sys.executable, "-m", "web_valueist",
        "http://example.com", "str", "ANY", "eq", "Example Domain", "--json"
    ]
    # This might fail if the selector 'ANY' doesn't match anything,
    # but we want to check how it's PARSED.
    # Actually evaluate will be called with url=http://example.com, parser=str, selector=ANY, operator=eq, value=Example Domain
    result = subprocess.run(cmd, capture_output=True, text=True, env={"PYTHONPATH": "."})
    # If selector 'ANY' is not found, it raises ValueNotFound and exits with 1.
    # But --json should still output something if it reached main?
    # Wait, if it raises ValueNotFound in __main__, it catches and exits 1.
    # Let's check stderr for "Error: Value not found" which means it parsed correctly.
    assert "Error: Value not found" in result.stderr
    # If it misparsed, it would probably complain about missing arguments or wrong operator.
