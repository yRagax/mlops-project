import os
import dotenv

dotenv.load_dotenv()
API_PORT = int(os.getenv("API_PORT"))


def test_demo_predict_house_value_result_good(mocker):
    mock_post = mocker.patch("demo.demo.requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"prediction": 3.8415413999999997}

    from demo.demo import predict_house_value

    input_data = {
        "api_url": f"http://api:{API_PORT}/predict",
        "longitude": "-122.3456",
        "latitude": "47.6397",
        "housing_median_age": "36.0",
        "total_rooms": "880.0",
        "total_bedrooms": "3",
        "population": "322.0",
        "households": "126.0",
        "median_income": "8.3252",
    }

    result = predict_house_value(**input_data)

    assert isinstance(result, dict)
    assert "prediction" in result
    assert isinstance(result["prediction"], float)
    assert result["prediction"] > 0

    mock_post.assert_called_once()


def test_demo_predict_house_value_result_bad_status(mocker):
    mock_post = mocker.patch("demo.demo.requests.post")
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal Server Error"

    from demo.demo import predict_house_value

    input_data = {
        "api_url": f"http://api:{API_PORT}/predict",
        "longitude": "-122.3456",
        "latitude": "47.6397",
        "housing_median_age": "36.0",
        "total_rooms": "880.0",
        "total_bedrooms": "3",
        "population": "322.0",
        "households": "126.0",
        "median_income": "8.3252",
    }

    result = predict_house_value(**input_data)

    assert isinstance(result, dict)
    assert "error" in result
    assert result["error"] == f"Error 500: Internal Server Error"

    mock_post.assert_called_once()


def test_demo_predict_house_value_result_bad_request():

    from demo.demo import predict_house_value

    input_data = {
        "api_url": f"http://api:{API_PORT}/predict",
        "longitude": "-122.3456",
        "latitude": "47.6397",
        "housing_median_age": "36.0",
        "total_rooms": "880.0",
        "total_bedrooms": "3",
        "population": "322.0",
        "households": "126.0",
        "median_income": "8.3252",
    }

    result = predict_house_value(**input_data)

    assert isinstance(result, dict)
    assert "error" in result
    assert (
        result["error"]
        == f"Request failed: HTTPConnectionPool(host='api', port={API_PORT}): Max retries exceeded with url: /predict (Caused by NameResolutionError(\"HTTPConnection(host='api', port={API_PORT}): Failed to resolve 'api' ([Errno -3] Temporary failure in name resolution)\"))"
    )
