import os

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from tornado.template import Loader
from tornado.web import RequestHandler


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

        # send message to your Slack!
        post_fields = {
            'text': self.request.body
        }
        request = Request(slack_webhook_url, urlencode(post_fields).encode())
        self.write("Sending to Slack!")
