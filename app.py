from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/sandra")
def hello_sandra():
    return "<p>Hello, Sandra!</p>"