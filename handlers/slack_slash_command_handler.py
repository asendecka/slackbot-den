import os
import json
import pytz
import requests
from datetime import datetime

from tornado.template import Loader
from tornado.web import HTTPError, RequestHandler
from tornado.escape import json_decode


SUPPORTED_CITIES = {
    'lagos': 'Africa/Lagos',
    'london': 'Europe/London',
    'new york': 'America/New_York',
    'warsaw': 'Europe/Warsaw',
}


class SlackSlashCommandHandler(RequestHandler):

    def default_response(self):
        cities = ', '.join(SUPPORTED_CITIES.keys())
        msg = 'You need to provide one of the supported cities. Choose one from: {}.'
        return {
            'text': msg.format(cities)
        }

    def current_time_response(self, city):
        tz = pytz.timezone(SUPPORTED_CITIES[city])
        current_time = datetime.now(tz=tz)

        return {
            'response_type': 'in_channel',
            'text': 'It\'s {}!'.format(current_time.strftime('%-I:%M%p'))
        }

    def post(self):
        # if token do not match Slack token, raise 404
        slack_token = os.environ.get('SLACK_TOKEN')
        token = self.get_argument('token')
        if token != slack_token:
            raise HTTPError(404)

        text = self.get_argument('text', '').lower()
        if text in SUPPORTED_CITIES:
            response = self.current_time_response(text)
        else:
            response = self.default_response()

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(response))
