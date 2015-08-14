#!/usr/bin/python
# coding: utf-8

import os, requests, argparse

# Make this script generic and able to be used by all GOV.UK teams.
# $ python walrus.py ZENDESK_ID #SLACK_CHANNEL
parser = argparse.ArgumentParser(description='Team config for the Zendesk Slack bot.')
parser.add_argument("team_zendesk_id", help="team zendesk id", type=int)
parser.add_argument("slack_channel", help="team slack channel: #name", type=str)
args = parser.parse_args()

zendesk_view_url = 'https://govuk.zendesk.com/api/v2/views/{0}/tickets.json?sort_by=updated_requester,asc'.format(args.team_zendesk_id)
response = requests.get(zendesk_view_url,
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

slack_data = "Here are your Zendesk tickets in order of most recently updated (limited to 5 :sunny:):\n"
for ticket in tickets[0:6]:
    # Link to the specific ticket when displaying its ID.
    slack_data += "<{0}{1}|{1}> – {2} by {3}\n".format("https://govuk.zendesk.com/agent/tickets/",
                                                      ticket['id'],
                                                      ticket['subject'],
                                                      get_requester_name(ticket['requester_id']))

# Send the message to Slack.
slack_payload = {"channel": args.slack_channel, "username": "walrus", "text": slack_data}
post_req = requests.post(os.environ['SLACK_WEBHOOK_URL'], json=slack_payload)

if post_req.status_code == 200:
  print "Posted."
else:
  print "Failed: {0}, {1}".format(post_req.status_code,post_req.text)
