import math
import json
from fastapi.testclient import TestClient
from api.api import api

client = TestClient(api)


def test_api_predict_good():
    input_data = {
        "longitude": "-122.3456",
        "latitude": "47.6397",
        "housing_median_age": "36.0",
        "total_rooms": "880.0",
        "total_bedrooms": "3",
        "population": "322.0",
        "households": "126.0",
        "median_income": "8.3252",
    }

    response = client.post("/predict", json=input_data)

    assert response.status_code == 200
    assert math.isclose(response.json()["prediction"], 4.110213039002661)


def test_api_predict_bad_data_type():
    input_data = {
        "longitude": "-122.3456",
        "latitude": "47.6397",
        "housing_median_age": "36.0",
        "total_rooms": "880.0",
        "total_bedrooms": "3",
        "population": "large",
        "households": "126.0",
        "median_income": "8.3252",
    }

    response = client.post("/predict", json=input_data)

    assert response.status_code == 422
    assert (
        json.loads(response.text)["detail"][0]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )


def test_api_predict_bad_data_missing():
    input_data = {
        "longitude": "-122.3456",
        "latitude": "47.6397",
        "housing_median_age": "36.0",
        "total_rooms": "880.0",
        "total_bedrooms": "3",
        "population": "-10.0",
        "households": "126.0",
    }

    response = client.post("/predict", json=input_data)

    assert response.status_code == 422
    assert json.loads(response.text)["detail"][0]["msg"] == "Field required"
