import requests
import pytest
import yaml

# Read configuration from config.yaml
with open("tests/pytests_config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Flask microservice Base URL
BASE_URL = config["Base Application URL"]

@pytest.fixture
def new_customer():
    # New customer creation fixture
    data = {"name": "Test User", "address": "1234 Test St"}
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 201
    return response.json()  # Return new customer's data

def test_get_all_customers():
    # Test retrieve all customers
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Убедитесь, что ответ является списком

def test_create_customer():
    # Test create new customer
    data = {"name": "New User", "address": "5678 New Ave"}
    response = requests.post(BASE_URL, json=data)
    assert response.status_code == 201
    customer = response.json()
    assert "customer_id" in customer
    assert customer["name"] == data["name"]
    assert customer["address"] == data["address"]

def test_get_customer(new_customer):
    # Test retrieve a customer by it's customer_id
    customer_id = new_customer["customer_id"]
    response = requests.get(f"{BASE_URL}/{customer_id}")
    assert response.status_code == 200
    customer = response.json()
    assert customer["customer_id"] == customer_id
    assert customer["name"] == new_customer["name"]
    assert customer["address"] == new_customer["address"]

def test_update_customer(new_customer):
    # Test customer update
    customer_id = new_customer["customer_id"]
    updated_data = {"name": "Updated User", "address": "Updated Address"}
    response = requests.put(f"{BASE_URL}/{customer_id}", json=updated_data)
    assert response.status_code == 200

    updated_customer = response.json()
    assert updated_customer["customer_id"] == customer_id
    assert updated_customer["name"] == updated_data["name"]
    assert updated_customer["address"] == updated_data["address"]

    # Database Update validation
    response = requests.get(f"{BASE_URL}/{customer_id}")
    assert response.status_code == 200
    customer = response.json()
    assert customer["name"] == updated_data["name"]
    assert customer["address"] == updated_data["address"]

def test_delete_customer(new_customer):
    # Test Delete Customer
    customer_id = new_customer["customer_id"]
    response = requests.delete(f"{BASE_URL}/{customer_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted"

    # Test delete non-existing customer
    response = requests.get(f"{BASE_URL}/{customer_id}")
    assert response.status_code == 404
    assert response.json()["error"] == "Customer not found"
