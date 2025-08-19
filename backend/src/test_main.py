from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_calculate_settlement():
    test_params = {
        "merchant": "98755d88-f00c-4e64-9cc4-546f882d67ed",
        "date": "2023-01-13",
    }
    response = client.get("/settlement/", params=test_params)
    assert response.status_code == 200
    assert response.json() == {
        "date": "2023-01-13",
        "merchant": "98755d88-f00c-4e64-9cc4-546f882d67ed",
        "refund": "1618.87",
        "sale": "27363.09",
        "total": "25744.22",
    }


def test_calculate_settlement_invalid_merchant():
    test_params = {
        "merchant": "qwertyuioo2341234dasd",
        "date": "2023-01-13",
    }
    response = client.get("/settlement/", params=test_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `q` at 1"
                },
                "input": "qwertyuioo2341234dasd",
                "loc": ["query", "merchant"],
                "msg": "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `q` at 1",
                "type": "uuid_parsing",
            }
        ]
    }


def test_calculate_settlement_invalid_date():
    test_params = {
        "merchant": "98755d88-f00c-4e64-9cc4-546f882d67ed",
        "date": "223-01-13",
    }
    response = client.get("/settlement/", params=test_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "error": "input is too short",
                },
                "input": "223-01-13",
                "loc": [
                    "query",
                    "date",
                ],
                "msg": "Input should be a valid date or datetime, input is too short",
                "type": "date_from_datetime_parsing",
            },
        ],
    }


def test_calculate_settlement_extra_params():
    test_params = {
        "merchant": "98755d88-f00c-4e64-9cc4-546f882d67ed",
        "date": "2023-01-13",
        "sql": "injection",
    }
    response = client.get("/settlement/", params=test_params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": "injection",
                "loc": [
                    "query",
                    "sql",
                ],
                "msg": "Extra inputs are not permitted",
                "type": "extra_forbidden",
            },
        ],
    }
