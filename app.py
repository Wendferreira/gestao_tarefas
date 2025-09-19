from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any

# SQLAlchemy (ORM)
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from sqlalchemy import Integer, String, Boolean, DateTime

# Criar instância da aplicação Flask
app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Mude isso em produção

# Persistência em arquivo JSON (para migração inicial)
DATA_FILE = Path("tarefas.json")


# =====================
# Banco de Dados (ORM)
# =====================


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    texto: Mapped[str] = mapped_column(String(255), nullable=False)
    concluida: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    prioridade: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 0-2
    created_at: Mapped[Any] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[Any] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "texto": self.texto,
            "concluida": self.concluida,
            "prioridade": self.prioridade,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# A URL do banco de dados é lida da variável de ambiente `DATABASE_URL`.
# Se não estiver definida, usa o SQLite local como fallback.
DB_URL = os.environ.get("DATABASE_URL", "sqlite:///tarefas.db").replace(
    "postgres://", "postgresql://"
)
engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(
    bind=engine, class_=Session, expire_on_commit=False, future=True
)


def init_db() -> None:
    Base.metadata.create_all(engine)


def migrate_from_json_if_needed() -> None:
    """Migra dados do tarefas.json para o banco, se o banco estiver vazio."""
    with SessionLocal() as session:
        has_any = session.scalar(select(Task.id).limit(1)) is not None
        if has_any:
            return

    if not DATA_FILE.exists():
        return

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return

    tarefas_json = data.get("tarefas", [])
    if not isinstance(tarefas_json, list) or not tarefas_json:
        return

    # Inserir mantendo os campos relevantes
    with SessionLocal() as session:
        for t in tarefas_json:
            try:
                texto = t.get("texto") or t.get("titulo") or ""
                if not texto:
                    continue
                prioridade = int(t.get("prioridade", 1))
                concluida = bool(t.get("concluida", False))
                session.add(
                    Task(
                        texto=texto,
                        prioridade=max(0, min(2, prioridade)),
                        concluida=concluida,
                    )
                )
            except Exception:
                continue
        session.commit()


def adicionar_tarefa(texto, prioridade: int | None = None):
    """
    Adiciona uma nova tarefa à lista global

    Args:
        texto (str): Texto da tarefa

    Returns:
        dict: Dicionário com a tarefa criada
    """
    # prioridade: 0=baixa, 1=média (default), 2=alta
    prioridade_normalizada = (
        1 if prioridade is None else max(0, min(2, int(prioridade)))
    )

    with SessionLocal() as session:
        task = Task(texto=texto, prioridade=prioridade_normalizada, concluida=False)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task.to_dict()


def completar_tarefa(id_tarefa):
    """
    Marca uma tarefa como concluída

    Args:
        id_tarefa (int): ID da tarefa a ser completada

    Returns:
        bool: True se a tarefa foi encontrada e marcada, False caso contrário
    """
    with SessionLocal() as session:
        task: Optional[Task] = session.get(Task, id_tarefa)
        if not task:
            return False
        task.concluida = True
        session.commit()
        return True


def editar_tarefa(
    tarefa_id: int, texto: str | None = None, prioridade: int | None = None
) -> Optional[Dict[str, Any]]:
    """
    Edita o texto e/ou a prioridade de uma tarefa existente.

    Args:
        tarefa_id (int): ID da tarefa a ser editada.
        texto (str, optional): Novo texto da tarefa.
        prioridade (int, optional): Nova prioridade da tarefa (0-2).

    Returns:
        dict | None: A tarefa atualizada ou None se não for encontrada.
    """
    with SessionLocal() as session:
        task: Optional[Task] = session.get(Task, tarefa_id)
        if not task:
            return None
        if texto is not None and texto.strip():
            task.texto = texto.strip()
        if prioridade is not None:
            task.prioridade = max(0, min(2, int(prioridade)))
        session.commit()
        return task.to_dict()


def get_all_tasks() -> List[Dict[str, Any]]:
    """Retorna todas as tarefas do banco de dados, ordenadas."""
    with SessionLocal() as session:
        rows: List[Task] = session.scalars(
            select(Task).order_by(
                Task.concluida.asc(), Task.prioridade.desc(), Task.id.desc()
            )
        ).all()
        return [t.to_dict() for t in rows]


# Rotas da aplicação web
@app.route("/")
def index():
    # Consulta ordenada: pendentes primeiro; prioridade alta→baixa; mais recentes primeiro
    tarefas_view = get_all_tasks()
    return render_template("index.html", tarefas=tarefas_view)


@app.route("/adicionar", methods=["POST"])
def adicionar_tarefa_web():
    """Adicionar nova tarefa via formulário web"""
    texto = request.form.get("texto")
    prioridade = request.form.get("prioridade")

    if texto:
        adicionar_tarefa(texto, prioridade)
        flash("Tarefa adicionada com sucesso!", "success")
    else:
        flash("Texto da tarefa é obrigatório!", "error")

    return redirect(url_for("index"))


@app.route("/completar/<int:tarefa_id>")
def completar_tarefa_web(tarefa_id):
    """Completar tarefa via interface web"""
    if completar_tarefa(tarefa_id):
        flash("Tarefa marcada como concluída!", "success")
    else:
        flash("Tarefa não encontrada!", "error")

    return redirect(url_for("index"))


@app.route("/editar/<int:tarefa_id>", methods=["POST"])
def editar_tarefa_web(tarefa_id):
    """Editar tarefa via formulário web (modal)"""
    texto = request.form.get("texto")
    prioridade = request.form.get("prioridade")

    if not texto:
        flash("O texto da tarefa não pode ser vazio!", "error")
    else:
        if editar_tarefa(tarefa_id, texto, prioridade):
            flash("Tarefa atualizada com sucesso!", "success")
        else:
            flash("Tarefa não encontrada!", "error")
    return redirect(url_for("index"))


@app.route("/remover/<int:tarefa_id>")
def remover_tarefa(tarefa_id):
    """Remover tarefa"""
    with SessionLocal() as session:
        task = session.get(Task, tarefa_id)
        if task:
            session.delete(task)
            session.commit()
            flash("Tarefa removida com sucesso!", "success")
        else:
            flash("Tarefa não encontrada!", "error")
    return redirect(url_for("index"))


@app.route("/api/tarefas")
def api_tarefas():
    """API para obter todas as tarefas em JSON"""
    return jsonify(get_all_tasks())


@app.route("/api/tarefas/<int:tarefa_id>")
def api_tarefa(tarefa_id):
    """API para obter uma tarefa específica em JSON"""
    with SessionLocal() as session:
        task = session.get(Task, tarefa_id)
        if task:
            return jsonify(task.to_dict())
        return jsonify({"error": "Tarefa não encontrada"}), 404


@app.route("/api/adicionar", methods=["POST"])
def api_adicionar_tarefa():
    """API para adicionar tarefa via JSON"""
    data = request.get_json()
    texto = data.get("texto")
    prioridade = data.get("prioridade")

    if not texto:
        return jsonify({"error": "Texto é obrigatório"}), 400

    nova = adicionar_tarefa(texto, prioridade)
    return jsonify(nova), 201


@app.route("/api/completar/<int:tarefa_id>", methods=["POST"])
def api_completar_tarefa(tarefa_id):
    """API para completar tarefa via JSON"""
    if completar_tarefa(tarefa_id):
        return jsonify({"message": "Tarefa completada com sucesso"}), 200
    else:
        return jsonify({"error": "Tarefa não encontrada"}), 404


@app.route("/api/editar/<int:tarefa_id>", methods=["PUT", "PATCH"])
def api_editar_tarefa(tarefa_id):
    """API para editar uma tarefa via JSON"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição JSON inválido"}), 400

    texto = data.get("texto")
    prioridade = data.get("prioridade")

    tarefa_atualizada = editar_tarefa(tarefa_id, texto, prioridade)
    if tarefa_atualizada:
        return jsonify(tarefa_atualizada), 200
    return jsonify({"error": "Tarefa não encontrada"}), 404


# Inicializa banco e migra dados do JSON (se necessário)
init_db()
migrate_from_json_if_needed()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
