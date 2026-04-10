from unittest.mock import patch
import web_valueist

def test_evaluate_unknown_quantifier_falls_back_to_any():
    """
    Test that an unknown quantifier string results in 'ANY' behavior.
    """
    # Mock _fetch_values to avoid real network/parsing calls
    # We patch it where it is used or defined. In this case, it's used in evaluate
    # which is in web_valueist.lib.
    with patch('web_valueist.lib._fetch_values') as mock_fetch:
        mock_fetch.return_value = ["100", "200"]

        # Case: "UNKNOWN" quantifier should act like "ANY"
        # 200 > 150 is true, so ANY > 150 is true.
        result = web_valueist.evaluate(
            url="http://example.com",
            selector=".price",
            parser_name="int",
            operator_name=">",
            value="150",
            quantifier="UNKNOWN" # type: ignore
        )

        assert result["success"] is True
        assert result["values"] == [100, 200]

        # Case: All fail
        result = web_valueist.evaluate(
            url="http://example.com",
            selector=".price",
            parser_name="int",
            operator_name=">",
            value="250",
            quantifier="UNKNOWN" # type: ignore
        )
        assert result["success"] is False
