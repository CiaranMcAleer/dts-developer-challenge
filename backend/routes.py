from flask import request, jsonify
from .app import app, get_db

@app.route('/ping')
def ping():
    return 'pong', 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(dict(task)), 200

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return jsonify([dict(task) for task in tasks]), 200

@app.route('/tasks/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    status = request.json.get('status')
    if not status:
        return jsonify({'error': 'Missing status field'}), 400

    db = get_db()
    cur = db.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Status updated'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cur = db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted'}), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    title = data.get('title')
    status = data.get('status')
    due_date = data.get('due_date')
    description = data.get('description', '')

    errors = {}
    if not title or not isinstance(title, str):
        errors['title'] = 'Title is required and must be a string.'
    if not status or not isinstance(status, str):
        errors['status'] = 'Status is required and must be a string.'
    if not due_date or not isinstance(due_date, str):
        errors['due_date'] = 'Due date is required and must be a string (ISO format).'
    if errors:
        return jsonify({'errors': errors}), 400

    db = get_db()
    cur = db.execute(
        'INSERT INTO tasks (title, description, status, due_date) VALUES (?, ?, ?, ?)',
        (title, description, status, due_date)
    )
    db.commit()
    task_id = cur.lastrowid
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    return jsonify(dict(task)), 201

