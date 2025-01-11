# Web Valueist

Fetches a value from the web, compares it with a given value and exits with zero
exit code if the condition is satisfied


## Setup

While in project directory:
```
./install.sh
```

## Usage:

`web_valueist [-h] [--debug] url parser_name selector operator_name value`

```
positional arguments:
  url
  parser_name
  selector
  operator_name
  value

options:
  -h, --help     show this help message and exit
  --debug

Did somebody say cron jobs? Have fun!
```

## Sample Usage

Sample success

```
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer ">" 240
```

( you can also use `gt` instead of `">"`)

Output:

```
INFO:__main__:Success: Condition satisfied
```

Exit Code: `0`

Sample failure

```
python -m web_valueist https://www.ikea.com.cy/en/products/fjallhavre-duvet-warm-240x220-cm/70458057/ int span.price__integer "<" 240
```

( you can also use `lt` instead of `"<"`)

Output:

```
ERROR:__main__:Failure: Condition not satisfied
```

Exit Code: `1`



### Sample cron job

```
*/30 * * * * web_valueist "https://www.bazaraki.com/car-motorbikes-boats-and-parts/cars-trucks-and-vans/mazda/mazda-mx5/year_min---71/?ordering=cheapest&lat=35.01804869361969&lng=34.04709596563199&radius=5000&price_max=30000" int .advert__content-price._not-title   "<" 22500 &&message="Some fancy car matching your criteria was found" &&command -v notify-send >/dev/null 2>&1 && notify-send $message || say $message
```