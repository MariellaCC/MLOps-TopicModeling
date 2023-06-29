import pytest 
import requests
#from requests.auth import HTTPBasicAuth

def test_api_working():
    response = requests.get('http://localhost:8000/')
    assert response.json() == "Hello, I'm working"


#def test_coherence_type():
#
#    data = {
#  "num_topic": 2,
#  "date_ref_1": "1940-06-06",
#  "date_ref_2": "1941-05-01"
#}
#    r = requests.post('http://localhost:8000/topic', json=data, auth=HTTPBasicAuth('admin', 'mdp'))
#    assert type(r.json()['coherence']) == float
#
#def test_user():
#
#    r = requests.post('http://localhost:8000/topic', auth=HTTPBasicAuth('fdmin', 'mdp'))
#    assert list(r.json().values())[0] == 'Incorrect email or password'