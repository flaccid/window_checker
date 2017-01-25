#!/usr/bin/env python

import argparse
import os
import json
import arrow
from datetime import date, time, timedelta
from dateutil.rrule import rrulestr

# start_hour, start_minute, start_rule, stop_hour, stop_minute, stop_rule
# Example - Weekdays 9am to 5pm
# start_hour: 9
# start_minute: 0
# start_rule: FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
# stop_hour: 17
# stop_minute: 0
# stop_rule: FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
# tz: Australia/Sydney

def on_today(dt, tz):
    on_today = (dt.date() == arrow.now(tz).date())
    return on_today

def window_check(start_hour, start_minute, start_rule, stop_hour, stop_minute, stop_rule, tz, debug=False):
    # convert certain keys back to int
    start_hour = int(start_hour)
    start_minute = int(start_minute)
    stop_hour = int(stop_hour)
    stop_minute = int(stop_minute)

    # first start and stop dates
    first_start_date = date.today() - timedelta(days=8)
    first_stop_date = date.today() - timedelta(days=8)
    first_start_dt = arrow.get(first_start_date.year,first_start_date.month,first_start_date.day,start_hour,start_minute,00,0,tz)
    first_stop_dt = arrow.get(first_stop_date.year,first_stop_date.month,first_stop_date.day,stop_hour,stop_minute,00,0,tz)
    first_start_year = first_start_date.year
    first_start_month = first_start_date.month
    first_start_day = first_start_date.day
    first_stop_year = first_stop_date.year
    first_stop_month = first_stop_date.month
    first_stop_day = first_stop_date.day

    # formulate rules and rulesets
    start_rr = "RRULE:{}".format(start_rule)
    start_rs = rrulestr(start_rr, dtstart=first_start_dt.datetime)

    stop_rr = "RRULE:{}".format(stop_rule)
    stop_rs = rrulestr(stop_rr, dtstart=first_stop_dt.datetime)

    # start and stop time within the given day if scheduled
    start_time = time(start_hour, start_minute)
    stop_time = time(stop_hour, stop_minute)

    # now
    now_dt = arrow.now(tz)

    # get the next and last occurrences
    last_start_dt = start_rs.before(now_dt.datetime, inc=True)
    next_start_dt = start_rs.after(now_dt.datetime, inc=True)
    last_stop_dt = stop_rs.before(now_dt.datetime, inc=True)
    next_stop_dt = stop_rs.after(now_dt.datetime, inc=True)

    params = [
        'first_start_date',
        'first_stop_date',
        'first_start_dt',
        'first_stop_dt',
        'start_minute',
        'start_hour',
        'first_start_day',
        'first_start_month',
        'first_start_year',
        'stop_minute',
        'stop_hour',
        'first_stop_day',
        'first_stop_month',
        'first_stop_year',
        'start_rs',
        'stop_rs',
        'tz',
        'now_dt',
        'last_start_dt',
        'next_start_dt',
        'last_stop_dt',
        'next_stop_dt',
    ]
    if debug:
        for p in params:
            print("{}: {}".format(p, eval(p)))

    schedule_info = {}
    schedule_info['event_active'] = 'false'
    schedule_info['start_rule'] = start_rr
    schedule_info['stop_rule'] = stop_rr
    schedule_info['start_time'] = start_time.isoformat()
    schedule_info['stop_time'] = stop_time.isoformat()
    schedule_info['next_start'] = next_start_dt.isoformat()
    schedule_info['next_stop'] = next_stop_dt.isoformat()
    schedule_info['last_start'] = last_start_dt.isoformat()
    schedule_info['last_stop'] = last_stop_dt.isoformat()
    schedule_info['timezone'] = tz
    schedule_info['now'] = now_dt.isoformat()

    if (on_today(last_start_dt, tz) and on_today(last_stop_dt, tz) and start_hour == 0 and start_minute == 0 and stop_hour == 0 and stop_minute == 0):
        # is on all day
        schedule_info['event_active'] = 'true'
    elif on_today(next_stop_dt, tz):
        if now_dt.datetime < next_stop_dt:
            if not on_today(next_start_dt, tz):
                schedule_info['event_active'] = 'true'

    return schedule_info

def lambda_handler(event, context):
    """AWS Lambda handler function."""

    params = {}
    keys = [
        'start_hour',
        'start_minute',
        'start_rule',
        'stop_hour',
        'stop_minute',
        'stop_rule',
        'tz'
    ]

    for key in keys:
        if key in os.environ:
            params[key] = os.environ[key]
        elif event:
            if key in event:
                params[key] = event[key]
            elif 'params' in event:
                if 'querystring' in event['params']:
                    params[key] = event['params']['querystring'][key]

    return window_check(eval(keys))

def cli():
    """Entrypoint from CLI."""

    # example commmand:
    # window_checker.py --start-hour 9 --start-minute 0 --stop-hour 17 --stop-minute 0 --tz 'Australia/Sydney' 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR'

    parser = argparse.ArgumentParser(
        description='Checks if an iCal event (RRULE) is currently active based on a start and stop time within a day period.')
    required = parser.add_argument_group('required arguments')
    required.add_argument('--start-hour', help='start hour of the event', required=True)
    required.add_argument('--start-minute', help='start minute of the event', required=True)
    required.add_argument('--stop-hour', help='stop hour of the event', required=True)
    required.add_argument('--stop-minute', help='stop minute of the event', required=True)
    parser.add_argument('--tz', help='the timezone')
    parser.add_argument('rrule', nargs='+', help='the RRULE to apply')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--json', '-j', action='count',
                        help='output values in json format')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--debug', '-d', action='count')
    args = parser.parse_args()

    window = window_check(
        args.start_hour,
        args.start_minute,
        args.rrule[0],
        args.stop_hour,
        args.stop_minute,
        args.rrule[0],
        args.tz,
        args.debug
    )
    if args.json:
        print(json.dumps(window))
    else:
        for k, v in window.items():
            print("{}: {}".format(k, v))

if __name__ == "__main__":
    cli()
