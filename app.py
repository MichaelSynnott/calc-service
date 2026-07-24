"""A tiny calculator web service for teaching.

Each endpoint reads two numbers, `a` and `b`, from the query string,
does one arithmetic operation, and returns the result as plain text.

Example:  http://localhost:8000/add?a=3&b=4   ->   3.0 + 4.0 = 7.0
"""

from flask import Flask, request

app = Flask(__name__)


def get_numbers():
    """Read `a` and `b` from the query string and convert them to floats.

    Raises ValueError if either parameter is missing or not a number.
    """
    a = request.args.get("a")
    b = request.args.get("b")
    if a is None or b is None:
        raise ValueError("Please supply both parameters, e.g. ?a=3&b=4")
    return float(a), float(b)


def get_single_number():
    """Read `a` from the query string and convert it to a float.

    Raises ValueError if the parameter is missing or not a number.
    """
    a = request.args.get("a")
    if a is None:
        raise ValueError("Please supply 'a', e.g. ?a=4")
    return float(a)


@app.route("/")
def home():
    return (
        "Calculator service is running. Try:\n"
        "  /add?a=3&b=4\n"
        "  /subtract?a=10&b=4\n"
        "  /multiply?a=6&b=7\n"
        "  /square?a=4\n"
        "  /power?a=2&b=3\n"
        "  /divide?a=10&b=4\n",
        200,
        {"Content-Type": "text/plain"},
    )


@app.route("/add")
def add():
    a, b = get_numbers()
    result = a + b
    return f"{a} + {b} = {result}"


@app.route("/subtract")
def subtract():
    a, b = get_numbers()
    result = a - b
    return f"{a} - {b} = {result}"


@app.route("/multiply")
def multiply():
    a, b = get_numbers()
    result = a * b
    return f"{a} * {b} = {result}"


@app.route("/power")
def power():
    a, b = get_numbers()
    result = a ** b
    return f"{a} ^ {b} = {result}"


@app.route("/square")
def square():
    a = get_single_number()
    result = a * a
    return f"{a} squared = {result}"


@app.route("/divide")
def divide():
    a, b = get_numbers()
    if b == 0:
        return "Cannot divide by zero", 400
    result = a / b
    return f"{a} / {b} = {result}"


@app.route("/modulo")
def modulo():
    a, b = get_numbers()
    if b == 0:
        return "Cannot perform modulo by zero", 400
    result = a % b
    return f"{a} % {b} = {result}"


@app.errorhandler(ValueError)
def bad_input(error):
    return f"Bad input: {error}", 400


if __name__ == "__main__":
    # host="0.0.0.0" makes the service reachable from other computers
    # on your network, not just this Mac.
    # Port 8000 is used because macOS reserves port 5000 for AirPlay.
    app.run(host="0.0.0.0", port=8000)
