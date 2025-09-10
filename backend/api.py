# Importação das bibliotecas
from flask import Flask, request, jsonify
from flask_cors import CORS

# Criação da aplicação Flask
app = Flask(__name__)
CORS(app)

# --- DADOS MOCKADOS FINAIS (PARA APRESENTAÇÃO INDIVIDUAL) ---

users = {
    1: {"id": 1, "name": "Guilherme Alves", "email": "alves@ifce.com", "password": "123"},
    2: {"id": 2, "name": "Guilherme Monteiro", "email": "monteiro@ifce.com", "password": "123"},
    3: {"id": 3, "name": "Paulo Cosmo", "email": "paulo@ifce.com", "password": "123"},
    4: {"id": 4, "name": "Reginaldo", "email": "reginaldo@ifce.com", "password": "123"}
}
next_user_id = 5

projects = {
    1: {"id": 1, "name": "Avaliação Final - PW1", "user_id": 4},
}
next_project_id = 2

tasks = {
    1: {"id": 1, "title": "Aprovar os alunos na matéria", "description": "Eles merecem kkkkkkkk", "status": "inprogress", "project_id": 1, "due_date": "2025-09-28"},
}
next_task_id = 2
# -------------------------------------------------------------------------

current_session = {"user_id": None}

def get_logged_user_id():
    user_id = current_session.get("user_id")
    if user_id is None:
        raise PermissionError("Acesso não autorizado. Faça o login primeiro.")
    return user_id

# --- ROTAS DE AUTENTICAÇÃO ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email'), data.get('password')
    for user in users.values():
        if user['email'] == email and user['password'] == password:
            current_session["user_id"] = user['id']
            return jsonify(user), 200
    return jsonify({"error": "Credenciais inválidas"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    current_session["user_id"] = None
    return jsonify({"message": "Logout bem-sucedido"}), 200

# --- CRUD COMPLETO PARA PROJETOS ---
@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    try:
        logged_user_id = get_logged_user_id()
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401

    if request.method == 'GET':
        user_projects = [p for p in projects.values() if p['user_id'] == logged_user_id]
        return jsonify(user_projects)
    
    if request.method == 'POST':
        global next_project_id
        data = request.json
        if not data or not data.get('name'):
            return jsonify({"error": "O nome do projeto é obrigatório"}), 400
        
        new_project = {"id": next_project_id, "name": data['name'], "user_id": logged_user_id}
        projects[next_project_id] = new_project
        next_project_id += 1
        return jsonify(new_project), 201

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        logged_user_id = get_logged_user_id()
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    
    if project_id not in projects or projects[project_id]['user_id'] != logged_user_id:
        return jsonify({"error": "Projeto não encontrado ou não autorizado"}), 404
    
    tasks_to_delete = [task_id for task_id, task in tasks.items() if task['project_id'] == project_id]
    for task_id in tasks_to_delete:
        del tasks[task_id]
        
    del projects[project_id]
    return jsonify({"message": "Projeto e suas tarefas foram deletados."})

# --- CRUD COMPLETO PARA TAREFAS ---
@app.route('/api/projects/<int:project_id>/tasks', methods=['GET'])
def get_tasks_for_project(project_id):
    try:
        logged_user_id = get_logged_user_id()
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401

    if project_id not in projects or projects[project_id]['user_id'] != logged_user_id:
        return jsonify({"error": "Projeto não encontrado ou não autorizado"}), 404
    project_tasks = [t for t in tasks.values() if t['project_id'] == project_id]
    return jsonify(project_tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        logged_user_id = get_logged_user_id()
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
        
    global next_task_id
    data = request.json
    title, project_id = data.get('title'), data.get('project_id')

    if not title or not project_id:
        return jsonify({"error": "Dados insuficientes"}), 400
    if project_id not in projects or projects[project_id]['user_id'] != logged_user_id:
        return jsonify({"error": "Projeto inválido ou não autorizado"}), 404
        
    new_task = {"id": next_task_id, "title": title, "description": "", "status": "todo", "project_id": project_id, "due_date": None}
    tasks[next_task_id] = new_task
    next_task_id += 1
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def handle_task(task_id):
    try:
        logged_user_id = get_logged_user_id()
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
        
    if task_id not in tasks:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    project_id = tasks[task_id]['project_id']
    if projects[project_id]['user_id'] != logged_user_id:
        return jsonify({"error": "Não autorizado"}), 403

    if request.method == 'PUT':
        data = request.json
        task = tasks[task_id]
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        task['status'] = data.get('status', task['status'])
        task['due_date'] = data.get('due_date', task['due_date'])
        return jsonify(task)

    if request.method == 'DELETE':
        del tasks[task_id]
        return jsonify({"message": "Tarefa deletada"})

if __name__ == '__main__':
    # O Render define a variável de ambiente PORT. Se não existir, usamos 5000 para testes locais.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)