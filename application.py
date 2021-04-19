from flask import Flask, render_template, redirect, jsonify, request


application = Flask(__name__)
application.config['SECRET_KEY'] = "ZhinZha"


def run(port=8080, host="127.0.0.1"):
    """Runs application on 'http://{host}:{port}/'"""
    application.run(port=port, host=host)
