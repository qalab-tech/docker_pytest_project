import requests
import yaml

# HEAD and OPTIONS HTTP-method TestCases

# Reading configuration from config.yaml
with open("tests/pytests_config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Flask microservice Base URL
BASE_URL = config["Base Application URL"]


def test_options():
    # Test Options HTTP Method
    response = requests.options(BASE_URL)
    assert response.status_code == 200
    assert response.headers['Allow'] == "OPTIONS, GET, POST, HEAD"

def test_head():
    # Test HEAD HTTP Method
    response = requests.options(BASE_URL)
    assert response.status_code == 200
    assert response.headers['CF-Cache-Status'] == "DYNAMIC"

