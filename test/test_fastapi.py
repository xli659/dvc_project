import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from fastapi_test import app

client = TestClient(app)

def test_api_locally_get_root():
    r = client.get("/")
    assert r.status_code == 200

def test_say_hello_with_slash():
    response = client.get("/test/")
    assert response.status_code == 200
    assert response.json() == {"greeting": "I have /"}

def test_say_hello_without_slash():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"greeting": "I dont have /"}

def test_create_item():
    payload = {"name": "item1", "tags": "tag1", "item_id": 1}
    response = client.post("/items/", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

def test_get_items():
    response = client.get("/items/123?count=2")
    assert response.status_code == 200
    assert response.json() == {"fetch": "Fetched 2 of 123"}

def test_exercise_function():
    payload = {"name": "item1", "tags": "tag1", "item_id": 1}
    response = client.post("/return/test_path?query=test_query", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "path": "test_path",
        "query": "test_query",
        "body": payload
    }