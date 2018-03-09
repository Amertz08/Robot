import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

import pytest

from flask import url_for

from factory import create_app
from models import db


@pytest.fixture
def app():
    return create_app('testing')

def setup_module(module):
    _app = app()
    with _app.app_context():
        db.create_all()

def teardown_module(module):
    _app = app()
    with _app.app_context():
        db.drop_all()

def test_index(client):
    resp = client.get(url_for('main.index'))
    assert resp.status_code == 200, f'Endpoint failed: {resp.status_code}'
