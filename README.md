<p align="center">
  <img src="logo.svg" alt="Web Valueist Logo">
</p>

# Web Valueist

[![PyPI version](https://badge.fury.io/py/web-valueist.svg)](https://badge.fury.io/py/web-valueist)
[![Python versions](https://img.shields.io/pypi/pyversions/web-valueist.svg)](https://pypi.org/project/web-valueist/)
[![License](https://img.shields.io/github/license/agalazis/web-valueist.svg)](https://github.com/agalazis/web-valueist/blob/main/LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/agalazis/web-valueist.svg)](https://github.com/agalazis/web-valueist/issues)
[![CI](https://github.com/agalazis/web-valueist/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/agalazis/web-valueist/actions/workflows/pypi-publish.yml)
[![Docs](https://github.com/agalazis/web-valueist/actions/workflows/docs-publish.yml/badge.svg)](https://web-valueist.csmonk.com/)

[Documentation Website](https://web-valueist.csmonk.com/)

Fetches a value from the web, compares it with a given value and exits with zero
exit code if the condition is satisfied


## Setup

While in project directory:
```bash
./install.sh
```

### Installation

You can install `web-valueist` from PyPI using your preferred package manager:

**pip:**
```bash
pip install web-valueist
```

**Poetry:**
```bash
poetry add web-valueist
```

**uv:**
```bash
uv pip install web-valueist
```

**pipenv:**
```bash
pipenv install web-valueist
```

## Usage:

`web_valueist [-h] [--debug] [--json] url parser_name [quantifier] selector operator_name value`

```text
positional arguments:
  url
  parser_name
  quantifier      Optional: ANY or EVERY (default: ANY)
  selector
  operator_name
  value

options:
  -h, --help      show this help message and exit
  --debug         Show debug logs including found values
  --json          Output input and result as JSON
```

## Sample Usage

By default, `web_valueist` is silent and communicates success or failure via the exit code.

Sample success

```bash
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer ">" 240
```

( you can also use `gt` instead of `">"`)

Exit Code: `0`

Sample failure

```bash
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer "<" 240
```

( you can also use `lt` instead of `"<"`)

Exit Code: `1`

### Debugging

Use the `--debug` flag to see the values fetched from the web.

```bash
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer ">" 240 --debug
```

Output:

```text
DEBUG:web_valueist.lib:Found value ['245']
```

### JSON Output

Use the `--json` flag to get a structured output.

```bash
python -m web_valueist http://example.com str h1 "eq" "Example Domain" --json
```

Output:
```json
{"args": {"url": "http://example.com", "parser_name": "str", "quantifier": "ANY", "selector": "h1", "operator_name": "eq", "value": "Example Domain"}, "result": {"success": true, "value": "Example Domain"}}
```

### Using Quantifiers

When a selector matches multiple elements, you can use `ANY` or `EVERY`.

- **ANY** (default): At least one selector match needs to satisfy the condition.
- **EVERY**: All selector matches need to satisfy the condition.

Example using `EVERY`:
```bash
python -m web_valueist https://example.com int EVERY .price ">" 100
```

If no quantifier is specified, `ANY` is used by default.

### Sample cron job

```bash
*/30 * * * * web_valueist "https://www.bazaraki.com/car-motorbikes-boats-and-parts/cars-trucks-and-vans/mazda/mazda-mx5/year_min---71/?ordering=cheapest&lat=35.01804869361969&lng=34.04709596563199&radius=5000&price_max=30000" int .advert__content-price._not-title   "<" 22500 &&message="Some fancy car matching your criteria was found" &&if command -v notify-send >/dev/null 2>&1 ; then notify-send "$message"; else say "$message"; fi
```
