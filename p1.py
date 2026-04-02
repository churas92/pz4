"""
Базовый файловый менеджер
"""

import os

class EmptyLineError(Exception):
    pass

def read_file_content(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            return [line.rstrip('\n') for line in lines]
    except FileNotFoundError:
        return []
    except PermissionError:
        print(f"Нет прав доступа к файлу '{filename}'")
        return None
    except UnicodeDecodeError:
        print(f"Неверная кодировка файла '{filename}'. Используйте UTF-8.")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файла: {e}")
        return None


def append_line_to_file(filename, line):
    try:
        if not line or line.strip() == "":
            raise EmptyLineError("Строка не может быть пустой")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(line + "\n")
        return True
    except EmptyLineError as e:
        print(f"Ошибка: {e}")
        return False
    except PermissionError:
        print(f"Ошибка: Нет прав доступа для записи в файл '{filename}'")
        return False
    except UnicodeEncodeError:
        print(f"Ошибка: Проблема с кодировкой. Убедитесь, что строка в кодировке UTF-8.")
        return False
    except Exception as e:
        print(f"Неизвестная ошибка при записи в файл: {e}")
        return False


def display_file_content(filename, lines):
    if lines is None:
        print("Невозможно отобразить содержимое файла.")
        return
    
    if not lines:
        print(f"Файл '{filename}' пуст.")
        return
    
    print(f"Содержимое файла '{filename}':")
    for i, line in enumerate(lines, 1):
        print(f"{i:3}. {line}")
    print(f"Всего строк: {len(lines)}\n")


def main():
    print("БАЗОВЫЙ ФАЙЛОВЫЙ МЕНЕДЖЕР")
    
    while True:
        filename = input("Введите имя файла (например, заметки.txt): ").strip()
        
        if not filename:
            print("Имя файла не может быть пустым. Попробуйте снова.")
            continue
        
        invalid_chars = '<>:"/\\|?*'
        if any(char in filename for char in invalid_chars):
            print(f"Имя файла содержит недопустимые символы: {invalid_chars}")
            print("Попробуйте другое имя.")
            continue
        
        break
    
    print(f"\nРабота с файлом: {filename}")
    
    print("Проверка существования файла...")
    current_content = read_file_content(filename)
    
    if current_content is None:
        print("Программа завершает работу из-за критической ошибки.")
        return
    elif current_content:
        print(f"Файл '{filename}' найден. Загружено {len(current_content)} строк.")
    else:
        print(f"Файл '{filename}' будет создан при первой записи.")
    
    while True:
        display_file_content(filename, current_content)

        print("\n ДОСТУПНЫЕ ДЕЙСТВИЯ:")
        print("1️  Добавить новую строку")
        print("2️  Показать содержимое")
        print("3  Выйти из программы")
        
        choice = input("\n Выберите действие (1-3): ").strip()
        
        if choice == "1":
            print("\n Введите текст для добавления (Enter - отмена):")
            line = input(">>> ").strip()
            
            if line == "":
                print(" Добавление строки отменено.")
                continue
            
            if append_line_to_file(filename, line):
                print(f" Строка успешно добавлена в файл '{filename}'!")
                new_content = read_file_content(filename)
                if new_content is not None:
                    current_content = new_content
                else:
                    print(" Не удалось обновить отображение содержимого.")
            else:
                print(" Не удалось добавить строку в файл.")
                
        elif choice == "2":
            print(" Обновление содержимого...")
            current_content = read_file_content(filename)
            if current_content is None:
                print(" Не удалось прочитать файл.")
            else:
                display_file_content(filename, current_content)
                
        elif choice == "3":
            break
            
        else:
            print(" Неверный выбор. Пожалуйста, выберите действие от 1 до 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Программа прервана пользователем.")
    except Exception as e:
        print(f"\n Критическая ошибка: {e}")
        print("Пожалуйста, перезапустите программу.")