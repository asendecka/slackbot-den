import json
import pytz
import logging
import os
import re
import time

from datetime import datetime

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.httpserver import HTTPServer
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import gen
from tornado import websocket
from tornado.web import Application
from slackclient import SlackClient

from handlers.slack_webhook_handler import SlackWebhookHandler
from handlers.slack_slash_command_handler import SlackSlashCommandHandler


logging.getLogger()


KEEP_ALIVE_FREQUENCY = 3  # in seconds


class SlackWebSocketClient():

    def __init__(self):
        self.slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
        self.slack_client = SlackClient(self.slack_bot_token)
        self.last_ping = 0

    @gen.coroutine
    def connect(self):
        logging.error('connect')
        self.slack_client.rtm_connect()

    @gen.coroutine
    def run(self):
        self.connect()
        while True:
            for message in self.slack_client.rtm_read():
                logging.error('message')
                logging.error(message)
                self.reply_to(message)
            self.keep_alive()
            time.sleep(1)


    @gen.coroutine
    def reply_to(self, message):
        if message is None:
            self.slack_client = None
            return

        if message and message['type'] == 'message':
            users = re.findall('<@(\w{9})>', message['text'])
            users = set(users)
            for user in users:
                user_data = self.slack_client.api_call('users.info', user=user)
                if user_data['user']['tz'] and not user_data['user']['is_bot']:
                    tz = pytz.timezone(user_data['user'].get('tz'))
                    current_time = datetime.now(tz=tz)
                    self.slack_client.api_call(
                        "chat.postMessage",
                        channel=message["channel"],
                        text="It's outside of @{}'s working hours ({} local time)".format(
                            user_data['user']['name'],
                            current_time.strftime('%-I:%M%p')
                        ),
                        as_user=True
                    )

    @gen.coroutine
    def keep_alive(self):
        logging.error(self.last_ping)
        now = int(time.time())
        if now > self.last_ping + KEEP_ALIVE_FREQUENCY:
            self.slack_client.server.ping()
            self.last_ping = now
