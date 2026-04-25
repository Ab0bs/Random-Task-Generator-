import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Файл для сохранения истории
HISTORY_FILE = "task_history.json"

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x400")

        # Предопределённые задачи с типами
        self.tasks = {
            "учёба": ["Прочитать статью", "Выучить 10 слов", "Решить 5 задач"],
            "спорт": ["Сделать зарядку", "Пробежать 3 км", "100 приседаний"],
            "работа": ["Проверить почту", "Составить отчёт", "Провести встречу"]
        }

        # Загрузка истории
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Выбор типа задачи
        ttk.Label(self.root, text="Тип задачи:").pack(pady=5)
        self.task_type = ttk.Combobox(
            self.root,
            values=["все"] + list(self.tasks.keys()),
            state="readonly"
        )
        self.task_type.set("все")
        self.task_type.pack(pady=5)

        # Кнопка генерации
        ttk.Button(
            self.root,
            text="Сгенерировать задачу",
            command=self.generate_task
        ).pack(pady=10)

        # Поле для отображения задачи
        self.current_task = ttk.Label(
            self.root,
            text="",
            wraplength=400,
            justify="center",
            font=("Arial", 12)
        )
        self.current_task.pack(pady=10)

        # Список истории
        ttk.Label(self.root, text="История задач:").pack(pady=5)
        self.history_list = tk.Listbox(self.root, height=10, width=60)
        self.history_list.pack(pady=5, padx=20, fill="both", expand=True)

        # Обновление списка истории
        self.update_history_list()

    def generate_task(self):
        selected_type = self.task_type.get()

        if selected_type == "все":
            all_tasks = [task for tasks in self.tasks.values() for task in tasks]
            task = random.choice(all_tasks)
        else:
            task = random.choice(self.tasks[selected_type])

        # Добавление в историю
        self.history.append(task)
        self.save_history()
        self.update_history_list()
        self.current_task.config(text=task)

    def update_history_list(self):
        self.history_list.delete(0, tk.END)
        for task in reversed(self.history):  # Новые сверху
            self.history_list.insert(tk.END, task)

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
