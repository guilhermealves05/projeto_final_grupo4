# Importação das bibliotecas
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração de CORS simplificada para aceitar todas as origens
CORS(app)

# --- DADOS MOCKADOS FINAIS (PARA APRESENTAÇÃO) ---
users = {
    1: {"id": 1, "name": "Guilherme Alves", "email": "alves@ifce.edu.br", "password": "123"},
    2: {"id": 2, "name": "Guilherme Monteiro", "email": "monteiro@ifce.edu.br", "password": "123"},
    3: {"id": 3, "name": "Paulo Cosmo", "email": "paulo@ifce.edu.br", "password": "123"},
    4: {"id": 4, "name": "Reginaldo", "email": "reginaldo@ifce.edu.br", "password": "123"}
}
next_user_id = 5

projects = {
    1: {"id": 1, "name": "Avaliação Final - PW1", "user_id": 4},
}
next_project_id = 2

tasks = {
    1: {"id": 1, "title": "Aprovar os alunos na matéria", "description": "Eles fizeram um ótimo trabalho!", "status": "inprogress", "project_id": 1, "due_date": "2025-12-15"},
}
next_task_id = 2
# -------------------------------------------------------------------------

current_session = {"user_id": None}

def get_logged_user_id():
    user_id = current_session.get("user_id")
    if user_id is None:
        raise PermissionError("Acesso não autorizado.")
    return user_id

# ROTA RAIZ PARA VERIFICAÇÃO DE SAÚDE
@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "API do Stellar Projects está no ar!"})

# --- ROTAS DA API (SIMPLIFICADAS, SEM /api) ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')
    for user in users.values():
        if user['email'] == email and user['password'] == password:
            current_session["user_id"] = user['id']
            return jsonify(user), 200
    return jsonify({"error": "Credenciais inválidas"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    current_session["user_id"] = None
    return jsonify({"message": "Logout bem-sucedido"}), 200

@app.route('/projects', methods=['GET', 'POST'])
def handle_projects():
    logged_user_id = get_logged_user_id()
    if request.method == 'GET':
        user_projects = [p for p in projects.values() if p['user_id'] == logged_user_id]
        return jsonify(user_projects)
    if request.method == 'POST':
        global next_project_id
        data = request.json
        new_project = {"id": next_project_id, "name": data['name'], "user_id": logged_user_id}
        projects[next_project_id] = new_project
        next_project_id += 1
        return jsonify(new_project), 201

@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    logged_user_id = get_logged_user_id()
    if project_id not in projects or projects[project_id]['user_id'] != logged_user_id:
        return jsonify({"error": "Projeto não encontrado"}), 404
    tasks_to_delete = [task_id for task_id, task in tasks.items() if task['project_id'] == project_id]
    for task_id in tasks_to_delete: del tasks[task_id]
    del projects[project_id]
    return jsonify({"message": "Projeto deletado."})

@app.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_tasks_for_project(project_id):
    logged_user_id = get_logged_user_id()
    if project_id not in projects or projects[project_id]['user_id'] != logged_user_id:
        return jsonify({"error": "Projeto não encontrado"}), 404
    project_tasks = [t for t in tasks.values() if t['project_id'] == project_id]
    return jsonify(project_tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    logged_user_id = get_logged_user_id()
    global next_task_id
    data = request.json
    title, project_id = data.get('title'), data.get('project_id')
    new_task = {"id": next_task_id, "title": title, "description": "", "status": "todo", "project_id": project_id, "due_date": None}
    tasks[next_task_id] = new_task
    next_task_id += 1
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def handle_task(task_id):
    logged_user_id = get_logged_user_id()
    if task_id not in tasks or projects[tasks[task_id]['project_id']]['user_id'] != logged_user_id:
        return jsonify({"error": "Não autorizado"}), 403
    if request.method == 'PUT':
        data = request.json
        tasks[task_id].update(data)
        return jsonify(tasks[task_id])
    if request.method == 'DELETE':
        del tasks[task_id]
        return jsonify({"message": "Tarefa deletada"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)