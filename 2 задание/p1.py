import json
import uuid

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.tasks = data
                else:
                    print("Данные в файле не являются списком задач")
                    self.tasks = []
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Неверный формат JSON в файле задач")
            self.tasks = []
        except Exception as e:
            print(f"Ошибка при загрузке задач: {e}")
            self.tasks = []
    
    def save_tasks(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении задач: {e}")
    
    def add_task(self, title, description):
        task = {
            "id": str(uuid.uuid4()),
            "название": title,
            "описание": description,
            "статус": "не выполнена"
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Задача добавлена с ID: {task['id']}")
    
    def view_tasks(self):
        if not self.tasks:
            print("Список задач пуст")
            return
        
        for task in self.tasks:
            if isinstance(task, dict):
                print(f"ID: {task.get('id', 'Нет ID')}")
                print(f"Название: {task.get('название', 'Нет названия')}")
                print(f"Описание: {task.get('описание', 'Нет описания')}")
                print(f"Статус: {task.get('статус', 'Нет статуса')}")
                print("-" * 30)
            else:
                print(f"Ошибка: Некорректный формат задачи: {task}")
    
    def mark_completed(self, task_id):
        for task in self.tasks:
            if isinstance(task, dict) and task.get("id") == task_id:
                task["статус"] = "выполнена"
                self.save_tasks()
                print(f"Задача {task_id} отмечена как выполненная")
                return
        print(f"Задача с ID {task_id} не найдена")
    
    def delete_task(self, task_id):
        for task in self.tasks:
            if isinstance(task, dict) and task.get("id") == task_id:
                confirm = input(f"Вы уверены, что хотите удалить задачу '{task.get('название', 'без названия')}'? (да/нет): ")
                if confirm.lower() == "да":
                    self.tasks.remove(task)
                    self.save_tasks()
                    print(f"Задача {task_id} удалена")
                else:
                    print("Удаление отменено")
                return
        print(f"Задача с ID {task_id} не найдена")

if __name__ == "__main__":
    manager = TaskManager()
    
    while True:
        print("\n=== Менеджер задач ===")
        print("1. Добавить задачу")
        print("2. Просмотреть все задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Удалить задачу")
        print("5. Выйти")
        
        choice = input("Выберите действие (1-5): ")
        
        if choice == "1":
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            manager.add_task(title, description)
        elif choice == "2":
            manager.view_tasks()
        elif choice == "3":
            task_id = input("Введите ID задачи: ")
            manager.mark_completed(task_id)
        elif choice == "4":
            task_id = input("Введите ID задачи: ")
            manager.delete_task(task_id)
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")