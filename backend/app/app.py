from flask import Flask

app = Flask(__name__)

def hello():
    return "Hello, World!"