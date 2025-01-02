# Web Valueist

Fetches a value from the web, compares it with a given value and exits with zero 
exit code if the condition is satisfied

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