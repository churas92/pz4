import json
import csv
import uuid

class StudentSystem:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_students()
    
    def load_students(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.students = data
                else:
                    print("Данные в файле не являются списком студентов")
                    self.students = []
        except FileNotFoundError:
            self.students = []
        except json.JSONDecodeError:
            print("Неверный формат JSON в файле студентов")
            self.students = []
        except Exception as e:
            print(f"Ошибка при загрузке студентов: {e}")
            self.students = []
    
    def save_students(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.students, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении студентов: {e}")
    
    def validate_age(self, age):
        try:
            age = int(age)
            if age > 16:
                return True, age
            else:
                print("Возраст должен быть больше 16 лет")
                return False, None
        except ValueError:
            print("Возраст должен быть числом")
            return False, None
    
    def validate_grades(self, grades_str):
        try:
            grades_list = [int(g.strip()) for g in grades_str.split(",") if g.strip()]
            for grade in grades_list:
                if grade < 2 or grade > 5:
                    print(f"Оценка {grade} не в диапазоне 2-5")
                    return False, None
            return True, grades_list
        except ValueError:
            print("Оценки должны быть числами")
            return False, None
    
    def add_student(self):
        print("\n Добавление студента ")
        
        name = input("Введите имя студента: ").strip()
        if not name:
            print("Имя не может быть пустым")
            return
        
        age_input = input("Введите возраст (> 16): ")
        is_valid_age, age = self.validate_age(age_input)
        if not is_valid_age:
            return
        
        group = input("Введите группу: ").strip()
        if not group:
            print("Группа не может быть пустой")
            return
        
        grades_input = input("Введите оценки (через запятую, от 2 до 5): ")
        is_valid_grades, grades = self.validate_grades(grades_input)
        if not is_valid_grades:
            return
        
        student = {
            "id": str(uuid.uuid4()),
            "имя": name,
            "возраст": age,
            "группа": group,
            "оценки": grades
        }
        
        self.students.append(student)
        self.save_students()
        print(f"Студент добавлен с ID: {student['id']}")
    
    def view_students(self):
        if not self.students:
            print("\nСписок студентов пуст")
            return
        
        print("\n Список студентов ")
        for student in self.students:
            if isinstance(student, dict):
                avg_grade = self.calculate_average_grade(student)
                print(f"ID: {student.get('id', 'Нет ID')}")
                print(f"Имя: {student.get('имя', 'Нет имени')}")
                print(f"Возраст: {student.get('возраст', 'Нет возраста')}")
                print(f"Группа: {student.get('группа', 'Нет группы')}")
                print(f"Оценки: {student.get('оценки', [])}")
                print(f"Средний балл: {avg_grade:.2f}")
                print("-" * 30)
    
    def search_students(self):
        if not self.students:
            print("\nСписок студентов пуст")
            return
        
        print("\n Поиск студентов ")
        print("1. Поиск по имени")
        print("2. Поиск по группе")
        
        choice = input("Выберите тип поиска (1-2): ")
        
        if choice == "1":
            name = input("Введите имя для поиска: ").strip().lower()
            results = [s for s in self.students if s.get("имя", "").lower() == name]
        elif choice == "2":
            group = input("Введите группу для поиска: ").strip().lower()
            results = [s for s in self.students if s.get("группа", "").lower() == group]
        else:
            print("Неверный выбор")
            return
        
        if results:
            print(f"\nНайдено {len(results)} студент(ов):")
            for student in results:
                avg_grade = self.calculate_average_grade(student)
                print(f"Имя: {student.get('имя')}, Группа: {student.get('группа')}, Средний балл: {avg_grade:.2f}")
        else:
            print("Студенты не найдены")
    
    def calculate_average_grade(self, student):
        grades = student.get("оценки", [])
        if grades:
            return sum(grades) / len(grades)
        return 0.0
    
    def show_average_grade(self):
        if not self.students:
            print("\nСписок студентов пуст")
            return
        
        print("\n Расчёт среднего балла ")
        student_id = input("Введите ID студента: ")
        
        for student in self.students:
            if student.get("id") == student_id:
                avg_grade = self.calculate_average_grade(student)
                print(f"Студент: {student.get('имя')}")
                print(f"Оценки: {student.get('оценки', [])}")
                print(f"Средний балл: {avg_grade:.2f}")
                return
        
        print(f"Студент с ID {student_id} не найден")
    
    def export_to_csv(self):
        if not self.students:
            print("\nНет данных для экспорта")
            return
        
        try:
            with open("students_export.csv", "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["ID", "Имя", "Возраст", "Группа", "Оценки", "Средний балл"])
                
                for student in self.students:
                    avg_grade = self.calculate_average_grade(student)
                    grades_str = ";".join(str(g) for g in student.get("оценки", []))
                    writer.writerow([
                        student.get("id", ""),
                        student.get("имя", ""),
                        student.get("возраст", ""),
                        student.get("группа", ""),
                        grades_str,
                        f"{avg_grade:.2f}"
                    ])
            
            print("Данные успешно экспортированы в файл 'students_export.csv'")
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")

if __name__ == "__main__":
    system = StudentSystem()
    
    while True:
        print("\n=== Система учёта студентов ===")
        print("1. Добавить студента")
        print("2. Просмотреть всех студентов")
        print("3. Поиск студентов")
        print("4. Расчёт среднего балла")
        print("5. Экспорт в CSV")
        print("6. Выйти")
        
        choice = input("Выберите действие (1-6): ")
        
        if choice == "1":
            system.add_student()
        elif choice == "2":
            system.view_students()
        elif choice == "3":
            system.search_students()
        elif choice == "4":
            system.show_average_grade()
        elif choice == "5":
            system.export_to_csv()
        elif choice == "6":
            print("пока")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")