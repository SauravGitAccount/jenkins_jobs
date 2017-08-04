#!/usr/bin/env python

import requests
import csv
import datetime
from datetime import date
from datetime import timedelta
import os

url = 'https://api.pagerduty.com/incidents'
yesterday = date.today() - timedelta(days=1)



def get_incidents(api_key, since=yesterday, until=date.today()):
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token=' + api_key
    }

    if isinstance(since, datetime.date):
        since = since.isoformat()
    if isinstance(until, datetime.date):
        until = until.isoformat()
    payload = {
        'since': since,
        'until': until
    }
    r = requests.get(url, headers=headers, params=payload)
    incidents = r.json()['incidents']


    csvfile = open('/tmp/pgdt_report.csv', 'w')
    fieldnames = ['id',
                  'incident_number',
                  'description',
                  'service_id',
                  'service_name',
                  'escalation_policy_id',
                  'escalation_policy_name',
                  'created_on',
                  'current_status',
                  'last_status_change_at',
                  'urgency'
                  ]
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in incidents:
        
        row = {
            'id': i['id'],
            'incident_number': i['incident_number'],
            'description': i['description'],
            'service_id': i['service']['id'],
            'service_name': i['service']['summary'],
            'escalation_policy_id': i['escalation_policy']['id'],
            'escalation_policy_name': i['escalation_policy']['summary'],
            'created_on': i['created_at'],
            'current_status': i['status'],
            'last_status_change_at': i['last_status_change_at'],
            'urgency': i['urgency']
        }
        writer.writerow(row)
    csvfile.close()

if __name__ == '__main__':
    get_incidents(api_key=os.environ['API_KEY'])