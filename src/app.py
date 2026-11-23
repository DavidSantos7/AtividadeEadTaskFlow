"""Aplicação web de gerenciamento ágil de tarefas da TechFlow Solutions."""
from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from flask import Flask, g, current_app, redirect, render_template_string, request, url_for, flash

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = Path(os.environ.get("TECHFLOW_DATABASE", BASE_DIR / "techflow.db"))

HTML = r"""<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TechFlow | Gestão de tarefas</title>
<style>
:root{--navy:#10243a;--blue:#1677d2;--cyan:#42c6df;--bg:#f3f6fa;--ink:#203247;--muted:#718096;--line:#e2e8f0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);font:15px/1.5 Inter,Segoe UI,Arial,sans-serif;color:var(--ink)}
header{background:linear-gradient(120deg,#10243a,#174c76);color:white;padding:26px max(5vw,20px);display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.brand{font-size:22px;font-weight:800;letter-spacing:.3px}.brand span{color:#52d3e8}.sub{color:#c7d8e8;font-size:13px}
main{max-width:1180px;margin:28px auto;padding:0 20px}.top{display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap}
h1{font-size:26px;margin:0 0 4px}.muted{color:var(--muted)}.stats{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}
.stat,.panel,.task{background:white;border:1px solid var(--line);border-radius:13px;box-shadow:0 4px 14px #1c35500a}
.stat{padding:13px 18px;min-width:125px}.stat b{display:block;font-size:23px;color:var(--navy)}.stat small{color:var(--muted)}
.layout{display:grid;grid-template-columns:340px 1fr;gap:18px;align-items:start}.panel{padding:20px}.panel h2{font-size:17px;margin:0 0 15px}
label{display:block;font-size:13px;font-weight:650;margin:12px 0 5px}
input,textarea,select{width:100%;padding:10px 11px;border:1px solid #ccd6e1;border-radius:8px;font:inherit;background:white;color:var(--ink)}
textarea{resize:vertical;min-height:76px}button,.btn{border:0;border-radius:8px;padding:10px 14px;background:var(--blue);color:white;font-weight:700;cursor:pointer;text-decoration:none;display:inline-block}
button:hover,.btn:hover{background:#0e5fae}.secondary{background:#eaf2fa;color:#245274}.danger{background:#fff0f0;color:#b42318}.actions{display:flex;gap:7px;flex-wrap:wrap}.actions button{padding:7px 10px;font-size:12px}
.boardhead{display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.filters{display:flex;gap:8px;flex-wrap:wrap}.filters select{width:auto;min-width:135px}
.columns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.column{background:#edf2f7;border-radius:12px;padding:11px;min-height:230px}.column h3{font-size:13px;text-transform:uppercase;letter-spacing:.7px;margin:3px 2px 11px;color:#53677d}
.task{padding:13px;margin-bottom:10px}.task h4{margin:0 0 6px;font-size:15px}.task p{font-size:13px;color:#64748b;margin:0 0 10px;white-space:pre-wrap}
.meta{display:flex;gap:6px;flex-wrap:wrap;margin:7px 0 11px}.tag{font-size:11px;padding:3px 8px;border-radius:30px;background:#eaf2fa;color:#245274}.high{background:#fff0e8;color:#b54708}.critical{background:#ffe4e4;color:#b42318}
.flash{padding:10px 13px;border-radius:8px;background:#e6f7ed;color:#17663a;margin:0 0 14px}
.empty{font-size:13px;color:#8290a0;text-align:center;padding:25px 5px}
@media(max-width:900px){.layout{grid-template-columns:1fr}.columns{grid-template-columns:1fr}} 
</style></head><body>
<header><div><div class="brand">Tech<span>Flow</span> Solutions</div><div class="sub">Painel ágil de operações logísticas</div></div><div class="sub">Organize • Priorize • Entregue</div></header>
<main>
{% with messages = get_flashed_messages() %}{% for message in messages %}<div class="flash">{{ message }}</div>{% endfor %}{% endwith %}
<div class="top"><div><h1>Quadro de tarefas</h1><div class="muted">Acompanhe o fluxo de trabalho da equipe em um só lugar.</div></div><div class="muted">Método Kanban</div></div>
<div class="stats">
<div class="stat"><b>{{ totals.total }}</b><small>Total de tarefas</small></div>
<div class="stat"><b>{{ totals.todo }}</b><small>A fazer</small></div>
<div class="stat"><b>{{ totals.progress }}</b><small>Em progresso</small></div>
<div class="stat"><b>{{ totals.done }}</b><small>Concluídas</small></div>
<div class="stat"><b>{{ totals.critical }}</b><small>Prioridade crítica</small></div>
</div>
<div class="layout">
<section class="panel"><h2>{{ 'Editar tarefa' if editing else 'Nova tarefa' }}</h2>
<form method="post" action="{{ url_for('update_task', task_id=editing.id) if editing else url_for('create_task') }}">
<label for="title">Título *</label><input id="title" name="title" maxlength="100" required value="{{ editing.title if editing else '' }}" placeholder="Ex.: Conferir rota de entrega">
<label for="description">Descrição</label><textarea id="description" name="description" maxlength="500" placeholder="Detalhes da atividade...">{{ editing.description if editing else '' }}</textarea>
<label for="priority">Prioridade</label><select id="priority" name="priority">
{% for p in ['Baixa','Média','Alta','Crítica'] %}<option value="{{ p }}" {% if editing and editing.priority == p %}selected{% elif not editing and p == 'Média' %}selected{% endif %}>{{ p }}</option>{% endfor %}
</select>
<label for="assignee">Responsável</label><input id="assignee" name="assignee" maxlength="60" value="{{ editing.assignee if editing else '' }}" placeholder="Nome do responsável">
<label for="status">Status</label><select id="status" name="status">{% for s in statuses %}<option value="{{ s }}" {% if editing and editing.status == s %}selected{% elif not editing and s == 'A Fazer' %}selected{% endif %}>{{ s }}</option>{% endfor %}</select>
<div class="actions" style="margin-top:16px"><button type="submit">{{ 'Salvar alterações' if editing else 'Adicionar tarefa' }}</button>{% if editing %}<a class="btn secondary" href="{{ url_for('index') }}">Cancelar</a>{% endif %}</div>
</form></section>
<section class="panel"><div class="boardhead"><h2 style="margin:0">Fluxo de trabalho</h2><form class="filters" method="get"><select name="priority" onchange="this.form.submit()"><option value="">Todas as prioridades</option>{% for p in ['Baixa','Média','Alta','Crítica'] %}<option value="{{ p }}" {% if selected_priority == p %}selected{% endif %}>{{ p }}</option>{% endfor %}</select><input name="q" value="{{ query }}" placeholder="Buscar tarefa..." style="max-width:180px"><button class="secondary" type="submit">Filtrar</button></form></div>
<div class="columns">{% for status in statuses %}<div class="column"><h3>{{ status }} · {{ grouped[status]|length }}</h3>
{% for task in grouped[status] %}<article class="task"><h4>{{ task.title }}</h4>{% if task.description %}<p>{{ task.description }}</p>{% endif %}
<div class="meta"><span class="tag {% if task.priority == 'Alta' %}high{% elif task.priority == 'Crítica' %}critical{% endif %}">{{ task.priority }}</span>{% if task.assignee %}<span class="tag">{{ task.assignee }}</span>{% endif %}</div>
<div class="actions"><a class="btn secondary" href="{{ url_for('edit_task', task_id=task.id) }}">Editar</a>
<form method="post" action="{{ url_for('move_task', task_id=task.id) }}"><input type="hidden" name="status" value="{{ next_status[status] }}"><button class="secondary" type="submit">{{ 'Avançar' if status != 'Concluído' else 'Reabrir' }}</button></form>
<form method="post" action="{{ url_for('delete_task', task_id=task.id) }}" onsubmit="return confirm('Excluir esta tarefa?')"><button class="danger" type="submit">Excluir</button></form></div></article>
{% else %}<div class="empty">Nenhuma tarefa nesta etapa.</div>{% endfor %}</div>{% endfor %}</div>
</section></div></main></body></html>"""

STATUSES = ["A Fazer", "Em Progresso", "Concluído"]
PRIORITIES = ["Baixa", "Média", "Alta", "Crítica"]

def connect_db():
    """Abre uma conexão SQLite associada à requisição atual."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    """Cria a tabela de tarefas quando o sistema é iniciado."""
    db = connect_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Média',
            assignee TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'A Fazer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = "techflow-development-key"
    app.config["DATABASE"] = str(DATABASE)
    if test_config:
        app.config.update(test_config)

    @app.before_request
    def prepare_database():
        init_db()

    @app.teardown_appcontext
    def close_db(error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.get("/")
    def index():
        db = connect_db()
        query = request.args.get("q", "").strip()
        priority = request.args.get("priority", "")
        sql = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if query:
            sql += " AND (title LIKE ? OR description LIKE ? OR assignee LIKE ?)"
            params.extend([f"%{query}%"] * 3)
        if priority in PRIORITIES:
            sql += " AND priority = ?"
            params.append(priority)
        tasks = db.execute(sql + " ORDER BY created_at DESC, id DESC", params).fetchall()
        grouped = {status: [dict(t) for t in tasks if t["status"] == status] for status in STATUSES}
        counts = {r["status"]: r["amount"] for r in db.execute("SELECT status, COUNT(*) amount FROM tasks GROUP BY status")}
        totals = {"total": sum(counts.values()), "todo": counts.get("A Fazer", 0),
                  "progress": counts.get("Em Progresso", 0), "done": counts.get("Concluído", 0),
                  "critical": db.execute("SELECT COUNT(*) FROM tasks WHERE priority='Crítica'").fetchone()[0]}
        return render_template_string(HTML, statuses=STATUSES, grouped=grouped, totals=totals,
            next_status={"A Fazer":"Em Progresso","Em Progresso":"Concluído","Concluído":"A Fazer"},
            editing=None, selected_priority=priority, query=query)

    def validate_form():
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Média")
        assignee = request.form.get("assignee", "").strip()
        status = request.form.get("status", "A Fazer")
        if not title:
            return None, "O título da tarefa é obrigatório."
        if priority not in PRIORITIES or status not in STATUSES:
            return None, "Prioridade ou status inválido."
        return (title, description, priority, assignee, status), None

    @app.post("/tasks")
    def create_task():
        values, error = validate_form()
        if error:
            flash(error)
            return redirect(url_for("index"))
        connect_db().execute("INSERT INTO tasks(title,description,priority,assignee,status) VALUES(?,?,?,?,?)", values)
        connect_db().commit()
        flash("Tarefa criada com sucesso.")
        return redirect(url_for("index"))

    @app.get("/tasks/<int:task_id>/edit")
    def edit_task(task_id):
        task = connect_db().execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if task is None:
            flash("Tarefa não encontrada.")
            return redirect(url_for("index"))
        tasks = connect_db().execute("SELECT * FROM tasks").fetchall()
        grouped = {s: [dict(t) for t in tasks if t["status"] == s] for s in STATUSES}
        counts = {r["status"]: r["amount"] for r in connect_db().execute("SELECT status, COUNT(*) amount FROM tasks GROUP BY status")}
        totals = {"total":sum(counts.values()),"todo":counts.get("A Fazer",0),"progress":counts.get("Em Progresso",0),
                  "done":counts.get("Concluído",0),"critical":connect_db().execute("SELECT COUNT(*) FROM tasks WHERE priority='Crítica'").fetchone()[0]}
        return render_template_string(HTML, statuses=STATUSES, grouped=grouped, totals=totals,
            next_status={"A Fazer":"Em Progresso","Em Progresso":"Concluído","Concluído":"A Fazer"},
            editing=dict(task), selected_priority="", query="")

    @app.post("/tasks/<int:task_id>")
    def update_task(task_id):
        values, error = validate_form()
        if error:
            flash(error)
            return redirect(url_for("edit_task", task_id=task_id))
        db = connect_db()
        if db.execute("SELECT id FROM tasks WHERE id=?", (task_id,)).fetchone() is None:
            flash("Tarefa não encontrada.")
            return redirect(url_for("index"))
        db.execute("UPDATE tasks SET title=?,description=?,priority=?,assignee=?,status=? WHERE id=?", (*values, task_id))
        db.commit()
        flash("Tarefa atualizada com sucesso.")
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/move")
    def move_task(task_id):
        status = request.form.get("status")
        if status not in STATUSES:
            flash("Status inválido.")
        else:
            connect_db().execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
            connect_db().commit()
            flash("Etapa da tarefa atualizada.")
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_id>/delete")
    def delete_task(task_id):
        connect_db().execute("DELETE FROM tasks WHERE id=?", (task_id,))
        connect_db().commit()
        flash("Tarefa excluída.")
        return redirect(url_for("index"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
