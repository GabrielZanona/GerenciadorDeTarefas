Gerenciador de Tarefas

O objetivo deste projeto é desenvolver uma aplicação web
utilizando Python, que simula as funcionalidades básicas de um
sistema de gerenciamento de tarefas, semelhante ao Trello. A
aplicação permitirá que os usuários gerencie suas tarefas,
incluindo funcionalidades como criar, editar, excluir e atribuir
tarefas a outros usuários, além de acompanhar o status das tarefas
(pendente, em andamento, concluída).

ESTE TRABALHO FOI FEITO POR :
- Alexandre Junior Longhini
- Gabriel Landarin Zanona
- Jon Albert Vianna

1. Crie um ambiente virtual:
    python -m venv venv

2. Ative o ambiente virtual:
    - No Windows:
        venv\Scripts\activate
    - No macOS/Linux:
        source venv/bin/activate

3. Instale as dependências:
    pip install -r requirements.txt

4. Configure o Banco de Dados:
    flask db init
    flask db migrate
    flask db upgrade

5. Execute o servidor:
   python run.py

A aplicação esta rodando na porta  http://127.0.0.1:5000/ (http://127.0.0.1:5000/login) para começar.

Rotas URL

- /register**: Página para registro de novos usuários.
- /login**: Página de login para usuários existentes.
- /logout: Encerra a sessão do usuário.
- /dashboard**: Painel principal onde o usuário pode ver e gerenciar suas tarefas.
- /task/new**: Rota para criar uma nova tarefa.
- /task/<id>/edit**: Rota para editar uma tarefa existente.
- /task/<id>/delete**: Rota para deletar uma tarefa específica.
- /users: Página para visualizar todos os usuários registrados e opções para apagar usuários.

Tecnologias Usadas

- Flask - Framework web para desenvolvimento da aplicação.
- Flask-Login - Gerenciamento de autenticação e sessão de usuários.
- Flask-WTF - Manuseio de formulários com validação.
- SQLite - Banco de dados para armazenamento das tarefas e usuários.
- Bootstrap  - Estilização da interface.
- Font Awesome - Ícones para aprimorar a interface visual.

