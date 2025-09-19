from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
from pathlib import Path

# Criar instância da aplicação Flask
app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Mude isso em produção

# Lista global de tarefas com ID incremental
tarefas = []
proximo_id = 1  # Contador global para IDs incrementais

# Persistência em arquivo JSON
DATA_FILE = Path("tarefas.json")


def carregar_dados() -> None:
    """Carrega tarefas e proximo_id do arquivo JSON, se existir."""
    global tarefas, proximo_id
    if not DATA_FILE.exists():
        # Inicializa arquivo com estrutura vazia
        salvar_dados()
        return
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            tarefas = data.get("tarefas", [])
            proximo_id = int(data.get("proximo_id", 1))
    except Exception:
        # Em caso de corrupção do arquivo, não quebra a aplicação
        tarefas = []
        proximo_id = 1


def salvar_dados() -> None:
    """Salva tarefas e proximo_id no arquivo JSON."""
    data = {
        "tarefas": tarefas,
        "proximo_id": proximo_id,
    }
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def adicionar_tarefa(texto, prioridade: int | None = None):
    """
    Adiciona uma nova tarefa à lista global

    Args:
        texto (str): Texto da tarefa

    Returns:
        dict: Dicionário com a tarefa criada
    """
    global proximo_id, tarefas

    # prioridade: 0=baixa, 1=média (default), 2=alta
    prioridade_normalizada = (
        1 if prioridade is None else max(0, min(2, int(prioridade)))
    )

    nova_tarefa = {
        "id": proximo_id,
        "texto": texto,
        "concluida": False,
        "prioridade": prioridade_normalizada,
    }

    tarefas.append(nova_tarefa)
    proximo_id += 1
    salvar_dados()

    return nova_tarefa


def completar_tarefa(id_tarefa):
    """
    Marca uma tarefa como concluída

    Args:
        id_tarefa (int): ID da tarefa a ser completada

    Returns:
        bool: True se a tarefa foi encontrada e marcada, False caso contrário
    """
    global tarefas

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["concluida"] = True
            salvar_dados()
            return True

    return False


# Rotas da aplicação web
@app.route("/")
def index():
    # Ordena: pendentes primeiro, depois concluídas; dentro do grupo, prioridade alta→baixa; em seguida, mais recentes primeiro
    tarefas.sort(
        key=lambda x: (
            x["concluida"],
            -(x.get("prioridade", 1)),
            -x["id"],
        )
    )
    return render_template("index.html", tarefas=tarefas)


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


@app.route("/remover/<int:tarefa_id>")
def remover_tarefa(tarefa_id):
    """Remover tarefa"""
    global tarefas
    tarefas = [t for t in tarefas if t["id"] != tarefa_id]
    salvar_dados()
    flash("Tarefa removida com sucesso!", "success")
    return redirect(url_for("index"))


@app.route("/api/tarefas")
def api_tarefas():
    """API para obter todas as tarefas em JSON"""
    return jsonify(tarefas)


@app.route("/api/tarefas/<int:tarefa_id>")
def api_tarefa(tarefa_id):
    """API para obter uma tarefa específica em JSON"""
    tarefa = next((t for t in tarefas if t["id"] == tarefa_id), None)
    if tarefa:
        return jsonify(tarefa)
    return jsonify({"error": "Tarefa não encontrada"}), 404


@app.route("/api/adicionar", methods=["POST"])
def api_adicionar_tarefa():
    """API para adicionar tarefa via JSON"""
    data = request.get_json()
    texto = data.get("texto")
    prioridade = data.get("prioridade")

    if not texto:
        return jsonify({"error": "Texto é obrigatório"}), 400

    nova_tarefa = adicionar_tarefa(texto, prioridade)
    return jsonify(nova_tarefa), 201


@app.route("/api/completar/<int:tarefa_id>", methods=["POST"])
def api_completar_tarefa(tarefa_id):
    """API para completar tarefa via JSON"""
    if completar_tarefa(tarefa_id):
        return jsonify({"message": "Tarefa completada com sucesso"}), 200
    else:
        return jsonify({"error": "Tarefa não encontrada"}), 404


carregar_dados()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
