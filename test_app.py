import pytest
from src.app import create_app

@pytest.fixture()
def client(tmp_path):
    database = tmp_path / "test.db"
    app = create_app({"TESTING": True, "DATABASE": str(database), "SECRET_KEY": "test"})
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Quadro de tarefas" in response.get_data(as_text=True)

def test_create_task(client):
    response = client.post("/tasks", data={
        "title": "Separar pedidos", "description": "Centro de distribuição",
        "priority": "Alta", "assignee": "Ana", "status": "A Fazer"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Separar pedidos" in response.get_data(as_text=True)

def test_title_is_required(client):
    response = client.post("/tasks", data={"title": "   "}, follow_redirects=True)
    assert "obrigatório" in response.get_data(as_text=True)

def test_update_task(client):
    client.post("/tasks", data={"title":"Tarefa antiga","priority":"Média","status":"A Fazer"})
    with client.application.app_context():
        from src.app import connect_db
        task_id = connect_db().execute("SELECT id FROM tasks").fetchone()["id"]
    response = client.post(f"/tasks/{task_id}", data={
        "title":"Tarefa revisada","priority":"Crítica","status":"Em Progresso"
    }, follow_redirects=True)
    assert "Tarefa revisada" in response.get_data(as_text=True)
    assert "Crítica" in response.get_data(as_text=True)

def test_move_and_delete_task(client):
    client.post("/tasks", data={"title":"Entregar pacote","priority":"Baixa","status":"A Fazer"})
    with client.application.app_context():
        from src.app import connect_db
        task_id = connect_db().execute("SELECT id FROM tasks").fetchone()["id"]
    client.post(f"/tasks/{task_id}/move", data={"status":"Em Progresso"})
    assert "Em Progresso" in client.get("/").get_data(as_text=True)
    client.post(f"/tasks/{task_id}/delete")
    assert "Entregar pacote" not in client.get("/").get_data(as_text=True)

def test_invalid_priority_is_rejected(client):
    response = client.post("/tasks", data={
        "title":"Teste", "priority":"Urgente demais", "status":"A Fazer"
    }, follow_redirects=True)
    assert "inválido" in response.get_data(as_text=True)
