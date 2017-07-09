import os
import requests

from tornado.template import Loader
from tornado.web import RequestHandler
from tornado.escape import json_decode


class SlackWebhookHandler(RequestHandler):
    def get(self):
        loader = Loader('templates')
        rendered = loader.load('slackbot_webhook.html').generate()
        self.write(rendered)

    def post(self):
        slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        if not slack_webhook_url:
            self.write("Slack webhook url not configured.")
            return

        # get message to send from POST
        message = self.get_argument('message')

        # send message to your Slack!
        post_fields = {
            'text': message
        }
        headers = {
            'content-type': 'application/json'
        }
        response = requests.post(slack_webhook_url, headers=headers, json=post_fields)
        self.write("Sending to Slack!")
