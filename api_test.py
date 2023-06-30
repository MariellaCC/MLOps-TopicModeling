import pytest 
import requests
from requests.auth import HTTPBasicAuth

def test_api_working():
    response = requests.get('http://localhost:8000/')
    assert response.json() == "Hello, I'm working"

def test_update_model_metrics():
    
    r = requests.put('http://localhost:8000/doc/update_model_metrics/10/', auth=HTTPBasicAuth('admin', 'mdp'))
    assert type(r.json()['coherence']) == float

def test_metrics():

    r = requests.post('http://localhost:8000/get_metrics', auth=HTTPBasicAuth('admin', 'mdp'))
    assert len(r.json()) == 3

def test_topic_from_new_text():
    data = {
  "file_name": "test_file",
  "file_content": "Mattia è un bimbo di 5 anni che passa tutte le sue giornate a disegnare. In realtà Mattia non si impegna più del necessario per tratteggiare le linee, fare bene le forme o rendere somiglianti le persone che disegna. Mattia ama soprattutto colorare, e ad ogni persona o cosa che disegna associa dei colori specifici. Ogni qual volta disegna suo papà Giuseppe, ad esempio, usa sempre gli stessi colori: i capelli li fa in nero, la maglia è azzurra e i pantaloni rigorosamente rossi. Il papà di Mattia non si veste ovviamente con colori così sgargianti, ma a Mattia piace immaginarlo così.",
  "date": "2001-05-03",
  "publication_name": "test",
  "publication_ref": "test"
}
    r = requests.put('http://localhost:8000/get_topic_from_new_text', json=data, auth=HTTPBasicAuth('admin', 'mdp'))
    assert type(r.json()['perplexity']) == float

def test_user():

    r = requests.put('http://localhost:8000/get_topic_from_new_text', auth=HTTPBasicAuth('fdmin', 'mdp'))
    assert r.json()['detail'] == 'Incorrect email or password'