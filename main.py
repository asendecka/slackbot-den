import json
import pytz
import logging
import os
import re

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
from handlers.slack_websocket_client import SlackWebSocketClient


logging.getLogger()


def main():
    client = SlackWebSocketClient()
    client.run()

    application = Application([
        (r'/whattime', SlackSlashCommandHandler),
        (r'/', SlackWebhookHandler),
    ])

    http_server = HTTPServer(application)
    port = int(os.environ.get('PORT', 8080))
    http_server.listen(port)


if __name__ == '__main__':
    main()
