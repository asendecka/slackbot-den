import os
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.template import Loader
from tornado.web import (
    Application,
    RequestHandler,
)


class SlackWebhookHandler(RequestHandler):
    def get(self):
        loader = Loader('templates')
        rendered = loader.load('slackbot_webhook.html').generate()
        self.write(rendered)


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
