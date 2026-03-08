# Web Valueist

Fetches a value from the web, compares it with a given value and exits with zero
exit code if the condition is satisfied


## Setup

While in project directory:
```
./install.sh
```

## Usage:

`web_valueist [-h] [--debug] [--json] url parser_name [quantifier] selector operator_name value`

```
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

```
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer ">" 240
```

( you can also use `gt` instead of `">"`)

Exit Code: `0`

Sample failure

```
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer "<" 240
```

( you can also use `lt` instead of `"<"`)

Exit Code: `1`

### Debugging

Use the `--debug` flag to see the values fetched from the web.

```
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer ">" 240 --debug
```

Output:

```
DEBUG:web_valueist.lib:Found value ['245']
```

### JSON Output

Use the `--json` flag to get a structured output.

```
python -m web_valueist http://example.com str h1 "eq" "Example Domain" --json
```

Output:
```json
{"args": {"url": "http://example.com", "parser_name": "str", "quantifier": "ANY", "selector": "h1", "operator_name": "eq", "value": "Example Domain"}, "result": {"success": true, "value": "Example Domain"}}
```

### Using Quantifiers

When a selector matches multiple elements, you can use `ANY` or `EVERY`.

```
python -m web_valueist https://example.com int ANY .price ">" 100
```

### Sample cron job

```
*/30 * * * * web_valueist "https://www.bazaraki.com/car-motorbikes-boats-and-parts/cars-trucks-and-vans/mazda/mazda-mx5/year_min---71/?ordering=cheapest&lat=35.01804869361969&lng=34.04709596563199&radius=5000&price_max=30000" int .advert__content-price._not-title   "<" 22500 &&message="Some fancy car matching your criteria was found" &&if command -v notify-send >/dev/null 2>&1 ; then notify-send "$message"; else say "$message"; fi
```
