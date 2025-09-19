# v0.1.0 — Primeira versão funcional

## Notas de Lançamento
- **App Flask completo**: UI com Bootstrap, rotas web e API
- **Tarefas com ID incremental** e status de conclusão
- **Prioridade**: Alta (2), Média (1), Baixa (0)
- **Ordenação**: pendentes primeiro; dentro do grupo: Alta > Média > Baixa; depois mais recentes
- **Persistência**: Utiliza SQLite com SQLAlchemy para armazenamento de dados. Migração inicial de `tarefas.json` se o banco estiver vazio.
- **Exemplo de uso**: script `exemplo_uso.py` para testar funções principais
- **CI**: GitHub Actions com flake8 e smoke test de import

## Funcionalidades
- `adicionar_tarefa(texto, prioridade)` → cria tarefa e retorna o objeto
- `completar_tarefa(id)` → marca tarefa como concluída
- **Rotas Web**:
  - `GET /` — página principal
  - `POST /adicionar` — adiciona tarefa (formulário com texto e prioridade)
  - `GET /completar/<id>` — completa tarefa
  - `GET /remover/<id>` — remove tarefa
- **API**:
  - `GET /api/tarefas` — lista JSON
  - `GET /api/tarefas/<id>` — detalhe JSON
  - `POST /api/adicionar` — body: `{ "texto": "...", "prioridade": 0|1|2 }`
  - `POST /api/completar/<id>` — completa

## Instalação e Execução
1. `py -m venv venv`
2. Ative o venv
3. `pip install -r requirements.txt`
4. `py app.py` e acesse `http://localhost:5000`

## Observações
- `tarefas.db` e `tarefas.json` estão no `.gitignore` (não são versionados)
- Workflow CI roda em pushes/PRs no branch `main`

## Arquivos Incluídos
- `app.py` — aplicação Flask principal
- `templates/index.html` — interface web
- `requirements.txt` — dependências Python
- `exemplo_uso.py` — exemplo de uso das funções
- `README.md` — documentação completa
- `CHANGELOG.md` — histórico de mudanças
- `.github/workflows/ci.yml` — GitHub Actions
