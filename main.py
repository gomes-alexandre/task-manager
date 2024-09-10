import tkinter as tk
from tkinter import messagebox
import sqlite3
from db import add_task, get_tasks, update_task, delete_task
import csv

# Função para sair
def exit_application():
    task_window.quit()  # Fecha a aplicação

# Função para abrir o gerenciador de tarefas
def open_task_manager(user_id):
    global root, frame_tasks
    root = tk.Tk()
    root.title("Gerenciador de Tarefas")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Layout do gerenciador de tarefas
    tk.Label(main_frame, text="Título").grid(row=0, column=0, padx=10, pady=5)
    entry_title = tk.Entry(main_frame)
    entry_title.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="Descrição").grid(row=1, column=0, padx=10, pady=5)
    entry_description = tk.Entry(main_frame)
    entry_description.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="Prioridade").grid(row=2, column=0, padx=10, pady=5)
    entry_priority = tk.Entry(main_frame)
    entry_priority.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(main_frame, text="Status").grid(row=3, column=0, padx=10, pady=5)
    entry_status = tk.Entry(main_frame)
    entry_status.grid(row=3, column=1, padx=10, pady=5)

    def add_task_button():
        title = entry_title.get()
        description = entry_description.get()
        priority = entry_priority.get()
        status = entry_status.get()
        add_task(user_id, title, description, priority, status, "Data de Criação")
        update_task_list()

    tk.Button(main_frame, text="Adicionar Tarefa", command=add_task_button).grid(row=4, column=1, padx=10, pady=10)

    # Filtro por status
    tk.Label(main_frame, text="Filtrar por status:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
    status_filter = tk.StringVar()
    status_filter.set("Todos")

    def filter_tasks():
        selected_status = status_filter.get()
        update_task_list(status=selected_status)

    tk.OptionMenu(main_frame, status_filter, "Todos", "Pendente", "Concluído").grid(row=6, column=1, padx=10, pady=5, sticky="ew")
    tk.Button(main_frame, text="Filtrar", command=filter_tasks).grid(row=6, column=2, padx=10, pady=5)

    # Exportar para CSV
    tk.Button(main_frame, text="Exportar Tarefas", command=export_tasks_to_csv).grid(row=7, column=1, padx=10, pady=10)

    frame_tasks = tk.Frame(root)
    frame_tasks.pack(padx=10, pady=10)

    update_task_list()

    root.mainloop()

def update_task_list(status="Todos"):
    for widget in frame_tasks.winfo_children():
        widget.destroy()

    tasks = get_tasks(user_id, status)
    for i, task in enumerate(tasks):
        tk.Label(frame_tasks, text=task[1], width=20).grid(row=i, column=0, padx=5, pady=5, sticky="w")
        tk.Label(frame_tasks, text=task[2], width=40).grid(row=i, column=1, padx=5, pady=5, sticky="w")
        tk.Label(frame_tasks, text=task[3], width=10).grid(row=i, column=2, padx=5, pady=5, sticky="w")
        tk.Label(frame_tasks, text=task[4], width=10).grid(row=i, column=3, padx=5, pady=5, sticky="w")

        # Botão para marcar como concluído
        tk.Button(frame_tasks, text="Concluir", command=lambda task=task: (update_task(task[0], task[1], task[2], task[3], "Concluído"), update_task_list())).grid(row=i, column=4, padx=5, pady=5)

        # Botão para editar a tarefa
        tk.Button(frame_tasks, text="Editar", command=lambda task=task: edit_task(task)).grid(row=i, column=5, padx=5, pady=5)

        # Botão para excluir a tarefa
        tk.Button(frame_tasks, text="Excluir", command=lambda task=task: (delete_task(task[0]), update_task_list())).grid(row=i, column=6, padx=5, pady=5)

def export_tasks_to_csv():
    tasks = get_tasks(user_id)
    with open('tarefas_exportadas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Título", "Descrição", "Prioridade", "Status", "Data de Criação"])
        for task in tasks:
            writer.writerow(task)

    tk.messagebox.showinfo("Exportar", "Tarefas exportadas com sucesso!")

def edit_task(task):
    # Abre uma nova janela para editar a tarefa
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Tarefa")

    tk.Label(edit_window, text="Título").grid(row=0, column=0, padx=10, pady=5)
    edit_title = tk.Entry(edit_window)
    edit_title.grid(row=0, column=1, padx=10, pady=5)
    edit_title.insert(0, task[1])

    tk.Label(edit_window, text="Descrição").grid(row=1, column=0, padx=10, pady=5)
    edit_description = tk.Entry(edit_window)
    edit_description.grid(row=1, column=1, padx=10, pady=5)
    edit_description.insert(0, task[2])

    tk.Label(edit_window, text="Prioridade").grid(row=2, column=0, padx=10, pady=5)
    edit_priority = tk.Entry(edit_window)
    edit_priority.grid(row=2, column=1, padx=10, pady=5)
    edit_priority.insert(0, task[3])

    tk.Label(edit_window, text="Status").grid(row=3, column=0, padx=10, pady=5)
    edit_status = tk.Entry(edit_window)
    edit_status.grid(row=3, column=1, padx=10, pady=5)
    edit_status.insert(0, task[4])

    def save_edits():
        update_task(task[0], edit_title.get(), edit_description.get(), edit_priority.get(), edit_status.get())
        edit_window.destroy()
        update_task_list()

    tk.Button(edit_window, text="Salvar", command=save_edits).grid(row=4, column=1, padx=10, pady=10)

    # **Botão de sair** (inserido após os outros botões)
    exit_button = tk.Button(task_window, text="Sair", command=exit_application, bg="red", fg="white")
    exit_button.grid(row=3, column=1, padx=10, pady=10)

    task_window.mainloop()