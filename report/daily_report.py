#!/usr/bin/env python
#
# Copyright (c) 2016, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of PagerDuty Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL PAGERDUTY INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests
import os
import csv
import datetime
from datetime import (date,timedelta)




# Update to match your API key

# Update to match your chosen parameters
SINCE = date.today() - timedelta(days=7)
UNTIL = date.today()
#DATE_RANGE = 'all'
#STATUSES = []
#INCIDENT_KEY = ''
#SERVICE_IDS = []
#TEAM_IDS = []
#USER_IDS = []
#URGENCIES = []
#TIME_ZONE = 'UTC'
#SORT_BY = []
#INCLUDE = []

def list_incidents(SINCE,UNTIL):
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=API_KEY)
    }
    payload = {
        'since': SINCE,
        'until': UNTIL,
        #'date_range': DATE_RANGE,
        #'statuses[]': STATUSES,
        #'incident_key': INCIDENT_KEY,
        #'service_ids[]': SERVICE_IDS,
        #'team_ids[]': TEAM_IDS,
        #'user_ids[]': USER_IDS,
        #'urgencies[]': URGENCIES,
        #'time_zone': TIME_ZONE,
        #'sort_by[]': SORT_BY,
        #'include[]': INCLUDE
    }
    r = requests.get(url, headers=headers, params=payload)
    print 'Status Code: {code}'.format(code=r.status_code)
    result = r.json()
    #print r.json()
    incidents = result['incidents']
    return incidents

def get_csv_report(SINCE,UNTIL):
    csvfile = open('report.csv', 'w')
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
    incidents = list_incidents(SINCE,UNTIL)
    for i in incidents:
        #r = requests.get('https://api.pagerduty.com/incidents/{0}/log_entries'.format(ea_id), headers=headers, stream=True)
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



def get_incident(ID):
    url = 'https://api.pagerduty.com/incidents/{id}'.format(id=ID)
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=API_KEY)
    }
    r = requests.get(url, headers=headers)
    print 'Status Code: {code}'.format(code=r.status_code)
    print r.json()

#Get the lists of incidents from the the past 1 days.
def get_daily_report():
    UNTIL = date.today()
    SINCE = UNTIL - timedelta(days=1)
    get_csv_report(SINCE,UNTIL)

#Get the list of incidents from the past 7 days till now
def get_weekly_report():
    UNTIL = date.today()
    SINCE = UNTIL - timedelta(days=7)
    get_csv_report(SINCE,UNTIL)


if __name__ == '__main__':

   API_KEY = os.environ['api_key']
   #SINCE = os.environ['since']
   #UNTIL = os.environ['until']
   if datetime.datetime.today().weekday() != 3:
       get_weekly_report()
   else:
       get_daily_report()



