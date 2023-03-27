from flask import Flask

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return (
        "Try /hello/Chris for parameterized Flask route.\n"
        "Try /module for module import guidance"
    )


@app.route("/hello/<name>", methods=['GET'])
def hello(name: str):
    return f"hello {name}"

