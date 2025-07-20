import os
import tempfile
import pytest
from flask import Flask
from backend.app import app as flask_app
from backend.db import init_db, get_db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['DATABASE'] = db_path
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            init_db()
        yield client
    os.close(db_fd)
    os.unlink(db_path)

def test_ping(client):
    rv = client.get('/ping')
    assert rv.status_code == 200
    assert rv.data == b'pong'

def test_create_and_get_task(client):
    # Create
    task = {
        'title': 'Test Task',
        'description': 'A test task',
        'status': 'pending',
        'due_date': '2025-07-21'
    }
    rv = client.post('/tasks', json=task)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['title'] == 'Test Task'
    task_id = data['id']

    # Get
    rv = client.get(f'/tasks/{task_id}')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['title'] == 'Test Task'

    # Get all
    rv = client.get('/tasks')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert any(t['id'] == task_id for t in data)

def test_update_task_status(client):
    # Create
    task = {
        'title': 'Status Task',
        'description': '',
        'status': 'pending',
        'due_date': '2025-07-21'
    }
    rv = client.post('/tasks', json=task)
    task_id = rv.get_json()['id']

    # Update status
    rv = client.patch(f'/tasks/{task_id}/status', json={'status': 'done'})
    assert rv.status_code == 200
    rv = client.get(f'/tasks/{task_id}')
    assert rv.get_json()['status'] == 'done'

def test_delete_task(client):
    # Create
    task = {
        'title': 'Delete Task',
        'description': '',
        'status': 'pending',
        'due_date': '2025-07-21'
    }
    rv = client.post('/tasks', json=task)
    task_id = rv.get_json()['id']

    # Delete
    rv = client.delete(f'/tasks/{task_id}')
    assert rv.status_code == 200
    # Confirm deletion
    rv = client.get(f'/tasks/{task_id}')
    assert rv.status_code == 404
