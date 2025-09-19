#!/usr/bin/env python3
"""
Exemplo de uso das funções adicionar_tarefa() e completar_tarefa()
"""

# Importar as funções do app.py
from app import adicionar_tarefa, completar_tarefa, tarefas


def main():
    print("=== Exemplo de uso das funções de tarefas ===\n")

    # Adicionar algumas tarefas
    print("1. Adicionando tarefas...")
    tarefa1 = adicionar_tarefa("Estudar Python")
    print(f"   Tarefa adicionada: {tarefa1}")

    tarefa2 = adicionar_tarefa("Fazer exercícios")
    print(f"   Tarefa adicionada: {tarefa2}")

    tarefa3 = adicionar_tarefa("Ler documentação")
    print(f"   Tarefa adicionada: {tarefa3}")

    print(f"\n2. Lista atual de tarefas:")
    for tarefa in tarefas:
        status = "✓ Concluída" if tarefa["concluida"] else "○ Pendente"
        print(f"   ID {tarefa['id']}: {tarefa['texto']} - {status}")

    # Completar algumas tarefas
    print(f"\n3. Completando tarefas...")
    resultado1 = completar_tarefa(1)  # Completar "Estudar Python"
    print(f"   Completar tarefa ID 1: {'Sucesso' if resultado1 else 'Falha'}")

    resultado2 = completar_tarefa(3)  # Completar "Ler documentação"
    print(f"   Completar tarefa ID 3: {'Sucesso' if resultado2 else 'Falha'}")

    # Tentar completar uma tarefa inexistente
    resultado3 = completar_tarefa(999)  # ID inexistente
    print(f"   Completar tarefa ID 999: {'Sucesso' if resultado3 else 'Falha'}")

    print(f"\n4. Lista final de tarefas:")
    for tarefa in tarefas:
        status = "✓ Concluída" if tarefa["concluida"] else "○ Pendente"
        print(f"   ID {tarefa['id']}: {tarefa['texto']} - {status}")

    print(f"\n5. Estatísticas:")
    total = len(tarefas)
    concluidas = sum(1 for t in tarefas if t["concluida"])
    pendentes = total - concluidas
    print(f"   Total: {total}")
    print(f"   Concluídas: {concluidas}")
    print(f"   Pendentes: {pendentes}")


if __name__ == "__main__":
    main()
