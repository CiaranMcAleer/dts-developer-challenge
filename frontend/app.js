const API_BASE = '/tasks';

function isoToLocal(iso) {
    if (!iso) return '';
    // Remove seconds for input compatibility
    return iso.slice(0, 16);
}

function localToIso(local) {
    if (!local) return '';
    // Add seconds for backend compatibility
    return local.length === 16 ? local + ':00' : local;
}

async function fetchTasks() {
    const res = await fetch(API_BASE);
    const tasks = await res.json();
    renderTasks(tasks);
}

function renderTasks(tasks) {
    const list = document.getElementById('task-list');
    list.innerHTML = '';
    if (!tasks.length) {
        list.innerHTML = '<em>No tasks found.</em>';
        return;
    }
    tasks.forEach(task => {
        const div = document.createElement('div');
        div.className = 'task';
        div.innerHTML = `
            <strong>${task.title}</strong> <br>
            <small>Status: ${task.status} | Due: ${task.due_date}</small><br>
            <div>${task.description || ''}</div>
            <div class="task-actions">
                <button onclick="editTask(${task.id})">Edit</button>
                <button onclick="deleteTask(${task.id})">Delete</button>
                <button onclick="updateStatus(${task.id}, 'completed')">Mark Completed</button>
            </div>
        `;
        list.appendChild(div);
    });
}

async function createTask(task) {
    const res = await fetch(API_BASE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task)
    });
    if (res.ok) {
        fetchTasks();
        resetForm();
    } else {
        alert('Failed to create task');
    }
}

async function updateTask(id, task) {
    // Only status can be updated via PATCH /tasks/<id>/status
    if ('status' in task && Object.keys(task).length === 1) {
        const res = await fetch(`${API_BASE}/${id}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: task.status })
        });
        if (res.ok) fetchTasks();
        else alert('Failed to update status');
        return;
    }
    // For full edit, delete and recreate (since only status PATCH is supported)
    await deleteTask(id, false);
    await createTask(task);
}

async function deleteTask(id, refresh = true) {
    const res = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
    if (res.ok && refresh) fetchTasks();
    else if (!res.ok) alert('Failed to delete task');
}

async function editTask(id) {
    const res = await fetch(`${API_BASE}/${id}`);
    if (!res.ok) return alert('Task not found');
    const task = await res.json();
    document.getElementById('task-id').value = task.id;
    document.getElementById('title').value = task.title;
    document.getElementById('description').value = task.description || '';
    document.getElementById('status').value = task.status;
    document.getElementById('due_date').value = isoToLocal(task.due_date);
    document.querySelector('button[type=submit]').textContent = 'Update Task';
    document.getElementById('cancel-edit').style.display = '';
}

async function updateStatus(id, status) {
    await updateTask(id, { status });
}

function resetForm() {
    document.getElementById('task-id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('description').value = '';
    document.getElementById('status').value = '';
    document.getElementById('due_date').value = '';
    document.querySelector('button[type=submit]').textContent = 'Add Task';
    document.getElementById('cancel-edit').style.display = 'none';
}

document.getElementById('task-form').onsubmit = async function(e) {
    e.preventDefault();
    const id = document.getElementById('task-id').value;
    const task = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        status: document.getElementById('status').value,
        due_date: localToIso(document.getElementById('due_date').value)
    };
    if (id) {
        await updateTask(id, task);
    } else {
        await createTask(task);
    }
};

document.getElementById('cancel-edit').onclick = resetForm;

fetchTasks();
