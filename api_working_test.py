import pytest 
import requests

def test_api_working():
    response = requests.get('http://localhost:8000/')
    assert response.json() == "Hello, I'm working"


def test_num_topic():

    data = {
  "num_topic": 2,
  "date_ref_1": "1940-06-06",
  "date_ref_2": "1941-05-01"
}
    r = requests.post('http://localhost:8000/topic', json=data)
    assert len(r.json()['topic'].keys()) == 