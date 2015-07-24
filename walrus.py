#!/usr/bin/python
# coding: utf-8

import os, requests

custom_formats_view_url = 'https://govuk.zendesk.com/api/v2/views/58638891/tickets.json?sort_by=updated_requester'
response = requests.get(custom_formats_view_url,
                        auth=(os.environ['ZENDESK_USERNAME'],
                              os.environ['ZENDESK_PASSWORD'])
                       ).json()

def get_requester_name(requester_id):
    requester = requests.get('https://govuk.zendesk.com/api/v2/users/{0}.json'.format(requester_id),
                             auth=(os.environ['ZENDESK_USERNAME'],
                                   os.environ['ZENDESK_PASSWORD'])
                                  ).json()
    return requester['user']['name']

tickets = response['tickets']

slack_data = "Here are your Zendesk tickets in order of most recently updated:\n"
for ticket in tickets:
    slack_data += "<{0}{1}|{1}> – {2} by {3}\n".format("https://govuk.zendesk.com/agent/tickets/",
                                                      ticket['id'],
                                                      ticket['subject'],
                                                      get_requester_name(ticket['requester_id']))

slack_payload = {"channel": "#custom", "username": "walrus", "text": slack_data}

post_req = requests.post(os.environ['SLACK_WEBHOOK_URL'], json=slack_payload)

if post_req.status_code == 200:
  print "Posted."
else:
  print "Failed: {0}, {1}".format(post_req.status_code,post_req.text)
