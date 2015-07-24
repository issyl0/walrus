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

for ticket in tickets:
    print "{0} – {1} – {2}".format(ticket['id'],
                                   ticket['subject'],
                                   get_requester_name(ticket['requester_id']))

