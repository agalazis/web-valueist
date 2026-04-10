import sys
from unittest.mock import MagicMock

# Mock dependencies that might be missing in the environment
# These must be mocked before any web_valueist module is imported.
if 'requests' not in sys.modules:
    sys.modules['requests'] = MagicMock()
if 'bs4' not in sys.modules:
    sys.modules['bs4'] = MagicMock()
