import os
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application

from handlers.slack_webhook_handler import SlackWebhookHandler


def main():
    application = Application([
        (r'/', SlackWebhookHandler),
    ])

    http_server = HTTPServer(application)
    port = int(os.environ.get('PORT', 8080))
    http_server.listen(port)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
