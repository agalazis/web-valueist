import sys
from unittest.mock import MagicMock, patch

# Note: In this environment, 'requests' and 'beautifulsoup4' (bs4) might not be installed.
# To allow the library modules to be imported and tested, we mock these dependencies
# at the module level if they are missing.
try:
    import requests
except ImportError:
    mock_requests = MagicMock()
    sys.modules['requests'] = mock_requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    mock_bs4 = MagicMock()
    sys.modules['bs4'] = mock_bs4

import pytest
from web_valueist.lib import _fetch_values, ValueNotFound

# We use @patch to mock the dependencies within the scope of the tests.
# This ensures that even if real dependencies are present, we use controlled mocks.
# If they are not present, we patch the 'sys.modules' versions we injected.

@patch('web_valueist.lib.requests.get')
@patch('web_valueist.lib.BeautifulSoup')
def test_fetch_values_single_value(mock_bs, mock_get):
    """
    Tests that _fetch_values correctly calls requests.get and BeautifulSoup
    to extract a single value from a provided selector.
    """
    url = "http://example.com"
    selector = ".price"
    html_content = "<html><body><span class='price'>100</span></body></html>"

    # Setup mock response from requests.get
    mock_response = MagicMock()
    mock_response.content = html_content.encode('utf-8')
    mock_response.text = html_content
    mock_get.return_value = mock_response

    # Setup mock soup and elements for BeautifulSoup
    mock_soup = MagicMock()
    mock_element = MagicMock()
    mock_element.text = "100"
    mock_soup.css.select.return_value = [mock_element]
    mock_bs.return_value = mock_soup

    result = _fetch_values(url, selector)

    # Verify the result
    assert result == ["100"]

    # Verify that requests.get was called with the correct URL and timeout
    mock_get.assert_called_once_with(url, timeout=10)

    # Verify that BeautifulSoup was initialized with the response content and 'html.parser'
    mock_bs.assert_called_once_with(mock_response.content, "html.parser")

    # Verify that the correct CSS selector was used
    mock_soup.css.select.assert_called_once_with(selector)

@patch('web_valueist.lib.requests.get')
@patch('web_valueist.lib.BeautifulSoup')
def test_fetch_values_multiple_values(mock_bs, mock_get):
    """
    Tests that _fetch_values correctly handles multiple matches for a selector.
    """
    url = "http://example.com"
    selector = ".price"

    mock_response = MagicMock()
    mock_get.return_value = mock_response

    mock_soup = MagicMock()
    mock_element1 = MagicMock()
    mock_element1.text = "100"
    mock_element2 = MagicMock()
    mock_element2.text = "200"
    mock_soup.css.select.return_value = [mock_element1, mock_element2]
    mock_bs.return_value = mock_soup

    result = _fetch_values(url, selector)

    assert result == ["100", "200"]

@patch('web_valueist.lib.requests.get')
@patch('web_valueist.lib.BeautifulSoup')
def test_fetch_values_not_found(mock_bs, mock_get):
    """
    Tests that ValueNotFound is raised when no elements match the selector.
    """
    url = "http://example.com"
    selector = ".non-existent"

    mock_response = MagicMock()
    mock_get.return_value = mock_response

    mock_soup = MagicMock()
    mock_soup.css.select.return_value = []
    mock_bs.return_value = mock_soup

    with pytest.raises(ValueNotFound):
        _fetch_values(url, selector)
