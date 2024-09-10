import sqlite3  # Adicionando a importação do sqlite3

# Função para criar as tabelas
def create_tables():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT,
            status TEXT,
            creation_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# Função para adicionar um novo usuário
def add_user(username, password):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    
    conn.commit()
    conn.close()

# Função para verificar usuário e senha no login
def verify_user(username, password):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()

    conn.close()
    return result

# Função para adicionar uma nova tarefa
def add_task(user_id, title, description, priority, status, creation_date):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tasks (user_id, title, description, priority, status, creation_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, title, description, priority, status, creation_date))

    conn.commit()
    conn.close()

# Função para obter todas as tarefas de um usuário
def get_tasks(user_id, status=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    if status and status != "Todos":
        cursor.execute('SELECT * FROM tasks WHERE user_id = ? AND status = ?', (user_id, status))
    else:
        cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))

    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Função para excluir uma tarefa
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    conn.commit()
    conn.close()

# Função para atualizar uma tarefa
def update_task(task_id, title, description, priority, status):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, priority = ?, status = ?
        WHERE id = ?
    ''', (title, description, priority, status, task_id))

    conn.commit()
    conn.close()