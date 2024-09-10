import tkinter as tk
from tkinter import messagebox
from db import create_tables, add_user, verify_user
from main import open_task_manager

# Cria as tabelas ao iniciar
create_tables()

# Função para realizar login
def login():
    username = entry_username.get()
    password = entry_password.get()

    user = verify_user(username, password)
    if user:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        root.destroy() # Fecha a tela de login
        open_task_manager(user[0])  # user[0] é o ID do usuário
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

# Função para sair
def exit_application():
    root.quit() # Fecha a aplicação

# Cria as tabelas no banco de dados ao iniciar o programa
create_tables()

def register():
    username = entry_username.get()
    password = entry_password.get()

    try:
        add_user(username, password)
        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
    except:
        messagebox.showerror("Erro", "Nome de usuário já existe.")

# Criação de interface de login
root = tk.Tk()
root.title("Login")

# Layout de login
tk.Label(root, text="Nome de usuário").grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Senha").grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Login", command=login).grid(row=2, column=0, padx=10, pady=10)
tk.Button(root, text="Cadastrar", command=register).grid(row=2, column=1, padx=10, pady=10)

# Botão sair
exit_button = tk.Button(root, text="Sair", command=exit_application, bg="red", fg="white")
exit_button.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()