from flask import Flask


application = Flask(__name__)


def run(port=8080, host="127.0.0.1"):
    """Runs application on 'http://{host}:{port}/'"""
    application.run(port=port, host=host)
