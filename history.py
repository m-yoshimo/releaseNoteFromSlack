#!/usr/bin/env python

from datetime import datetime
import os
import sys
import calendar
import requests
import json

url = 'https://slack.com/api/channels.history'
token = os.environ['SLACK_API_TOKEN']
channel_id = os.environ['SLACK_CHANNEL_ID']
date_yy_mm = os.environ['HISTORY_REQUEST_YY_MM']

def main():
    year = int(date_yy_mm.split('-')[0])
    month = int(date_yy_mm.split('-')[1])
    _, lastday = calendar.monthrange(year, month)

    oldest = datetime.strptime(date_yy_mm + "-01", '%Y-%m-%d').timestamp()
    latest = datetime.strptime(date_yy_mm + "-" + str(lastday), '%Y-%m-%d').timestamp()
    payload = {
        'token': token,
        'channel': channel_id,
        'latest': str(latest),
        'oldest': str(oldest)
    }
    r = requests.get(url, params=payload)
    if r.status_code != 200:
        print('Failed to get response (' + r.status_code + ')')
        sys.exit(1)

    json = r.json()
    ok = json['ok']
    if ok is False:
        print('Failed to get messages')
        print(json['error'])
        sys.exit(1)
    else:
        msgs = json['messages']
        for msg in msgs:
            date = datetime.fromtimestamp(int(float(msg['ts'])))
            message = msg['text'].replace('\u2022', '+')
            out = []
            for line in message.splitlines():
                if line.find('[confidential]') > 0:
                    continue
                out.append(line)
            print("### " + str(date.date()))
            print('\n'.join(out))
            print()

if __name__ == '__main__':
    main()
