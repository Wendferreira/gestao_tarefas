# Sistema de Gestão de Tarefas

Um aplicativo web simples para gerenciar tarefas, construído com Flask.

## Funcionalidades

- ✅ Adicionar novas tarefas
- ✅ Marcar tarefas como concluídas
- ✅ Remover tarefas
- ✅ Visualizar estatísticas (total, pendentes, concluídas)
- ✅ Interface responsiva com Bootstrap
- ✅ API REST para integração

## Pré-requisitos

- Python 3.7+
- Flask 3.1.2

## Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se estiver usando git
   git clone <url-do-repositorio>
   cd gestao_tarefas
   ```

2. **Crie um ambiente virtual**
   ```bash
   py -m venv venv
   ```

3. **Ative o ambiente virtual**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (CMD)
   venv\Scripts\activate.bat
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## Como executar

1. **Ative o ambiente virtual** (se não estiver ativo)
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Execute a aplicação**
   ```bash
   py app.py
   ```

3. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## Estrutura do Projeto

```
gestao_tarefas/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
├── templates/            # Templates HTML
│   └── index.html        # Página principal
└── venv/                 # Ambiente virtual (não versionado)
```

## API Endpoints

- `GET /` - Página principal
- `POST /adicionar` - Adicionar nova tarefa
- `GET /concluir/<id>` - Marcar tarefa como concluída
- `GET /remover/<id>` - Remover tarefa
- `GET /api/tarefas` - Listar todas as tarefas (JSON)
- `GET /api/tarefas/<id>` - Obter tarefa específica (JSON)

## Exemplo de Uso da API

```bash
# Obter todas as tarefas
curl http://localhost:5000/api/tarefas

# Obter tarefa específica
curl http://localhost:5000/api/tarefas/1
```

## Personalização

- **Chave secreta**: Altere `app.secret_key` em `app.py` para produção
- **Banco de dados**: Substitua a lista `tarefas` por um banco de dados real
- **Estilos**: Modifique o CSS em `templates/index.html`
- **Funcionalidades**: Adicione novas rotas em `app.py`

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Ícones**: Font Awesome
- **Templates**: Jinja2

## Próximos Passos

- [ ] Implementar banco de dados (SQLite/PostgreSQL)
- [ ] Adicionar autenticação de usuários
- [ ] Implementar categorias de tarefas
- [ ] Adicionar datas de vencimento
- [ ] Implementar busca e filtros
- [ ] Adicionar testes unitários

## Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.
# gestao_tarefas
