# window_checker

Checks if an iCal event (RRULE) is currently active based on a start and stop time within a day period.

## Usage

### Python

```
>>> import window_checker
>>> window_checker.window_check(start_hour=9, start_minute=0, start_rule='FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR', stop_hour=17, stop_minute=0, stop_rule='FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR', tz='Australia/Sydney')
{'last_stop': '2017-01-25T17:00:00+11:00', 'stop_rule': 'RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR', 'start_time': '09:00:00', 'start_rule': 'RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR', 'timezone': 'Australia/Sydney', 'stop_time': '17:00:00', 'last_start': '2017-01-25T09:00:00+11:00', 'event_active': 'false', 'now': '2017-01-25T20:01:09.744085+11:00', 'next_start': '2017-01-26T09:00:00+11:00', 'next_stop': '2017-01-26T17:00:00+11:00'}
```

### Command Line

See `window_checker.py --help`

### AWS Lambda

 1. Create the zip file using `make zip`
 2. Upload the code to AWS Lambda using the zip file
 3. Set the configuration to use `timezone_converter.lambda_handler` as the handler of the function.

## Useful Resources

 * https://nylas.com/blog/rrules/
 * http://crsmithdev.com/arrow/
 * https://julien.danjou.info/blog/2015/python-and-timezones
 * https://coderwall.com/p/7t3qdq/datetimes-and-timezones-and-dst-oh-my
 * https://labix.org/python-dateutil
 * https://dateutil.readthedocs.io/en/stable/
 * http://www.kanzaki.com/docs/ical/rrule.html

License and Authors
-------------------
- Author: Chris Fordham (<chris@fordham-nagy.id.au>)

```text
Copyright 2017, Chris Fordham

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
