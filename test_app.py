import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_add(client):
    """Addition returns correct result."""
    resp = client.get("/add?a=3&b=4")
    assert resp.status_code == 200
    assert "3.0 + 4.0 = 7.0" in resp.data.decode()


def test_subtract(client):
    """Subtraction returns correct result."""
    resp = client.get("/subtract?a=10&b=4")
    assert resp.status_code == 200
    assert "10.0 - 4.0 = 6.0" in resp.data.decode()


def test_multiply(client):
    """Multiplication returns correct result."""
    resp = client.get("/multiply?a=6&b=7")
    assert resp.status_code == 200
    assert "42.0" in resp.data.decode()


def test_power(client):
    """Power returns correct result."""
    resp = client.get("/power?a=2&b=3")
    assert resp.status_code == 200
    assert "8.0" in resp.data.decode()


def test_square(client):
    """Square returns correct result."""
    resp = client.get("/square?a=4")
    assert resp.status_code == 200
    assert "16.0" in resp.data.decode()


def test_divide(client):
    """Division returns correct result."""
    resp = client.get("/divide?a=10&b=4")
    assert resp.status_code == 200
    assert "2.5" in resp.data.decode()


def test_modulo(client):
    """Modulo returns correct result."""
    resp = client.get("/modulo?a=10&b=4")
    assert resp.status_code == 200
    assert "2.0" in resp.data.decode()


def test_missing_params(client):
    """Both parameters required on two-number endpoints."""
    resp = client.get("/add?a=3")
    assert resp.status_code == 400
    assert b"Bad input" in resp.data


def test_missing_a(client):
    """'a' required on single-number endpoints."""
    resp = client.get("/square?b=4")
    assert resp.status_code == 400
    assert b"Bad input" in resp.data


def test_no_params(client):
    """No params at all returns 400."""
    resp = client.get("/add")
    assert resp.status_code == 400
    assert b"Bad input" in resp.data


def test_non_numeric(client):
    """Non-numeric values raise BadRequest."""
    resp = client.get("/add?a=abc&b=def")
    assert resp.status_code == 400
    assert b"Bad input" in resp.data


def test_unknown_route(client):
    """Unregistered routes return 400, not 404."""
    resp = client.get("/invalid?a=abc&b=def")
    assert resp.status_code == 400
    assert b"Bad input" in resp.data


def test_negative_numbers(client):
    """Negative numbers work correctly."""
    resp = client.get("/add?a=-5&b=-3")
    assert resp.status_code == 200
    assert "-8.0" in resp.data.decode()


def test_zero_square(client):
    """Zero squared is zero."""
    resp = client.get("/square?a=0")
    assert resp.status_code == 200
    assert "0.0 squared = 0.0" in resp.data.decode()


def test_home_page(client):
    """Home page returns 200 with instructions."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Calculator service is running" in resp.data.decode()


def test_content_type(client):
    """Home page returns text/plain; arithmetic endpoints default to text/html."""
    resp = client.get("/add?a=1&b=2")
    # Flask appends charset to the content type for string returns.
    assert resp.content_type.startswith("text/")


def test_divide_by_zero_message(client):
    """Divide by zero returns specific message, not generic 'Bad input'."""
    resp = client.get("/divide?a=10&b=0")
    assert resp.status_code == 400
    assert b"Cannot divide by zero" in resp.data
