## v0.1.0 - 2025-09-19

Primeira versão funcional do projeto Gestão de Tarefas.

### Destaques
- Aplicativo Flask básico com rotas de interface e API
- Lista global de tarefas com ID incremental
- Funções utilitárias: `adicionar_tarefa(texto, prioridade)`, `completar_tarefa(id)` e `get_all_tasks()`
- Campo de prioridade (0=Baixa, 1=Média, 2=Alta)
- Ordenação: pendentes primeiro, depois concluídas; dentro do grupo: Alta > Média > Baixa; e mais recentes primeiro
- Persistência de dados com SQLite e SQLAlchemy (com migração inicial de `tarefas.json` se existir)
- UI responsiva com Bootstrap e badges de prioridade
- Exemplo de uso em `exemplo_uso.py`

### Endpoints
- `GET /` — página principal
- `POST /adicionar` — adiciona tarefa (formulário com texto e prioridade)
- `GET /completar/<id>` — completa tarefa
- `GET /remover/<id>` — remove tarefa
- `GET /api/tarefas` — lista JSON
- `GET /api/tarefas/<id>` — detalhe JSON
- `POST /api/adicionar` — cria tarefa via JSON `{ texto, prioridade }`
- `POST /api/completar/<id>` — completa via API

### Infra
- `.gitignore` com `venv/`, caches e `tarefas.json`, `tarefas.db`
- GitHub Actions: lint (flake8) e smoke test de import
