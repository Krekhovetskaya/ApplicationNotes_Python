import json
import random
import sys
from datetime import datetime
from os import path

from note import Note, NoteEncoder

command_list = {
    "Добавление новой заметки": "add",
    "Изменение заметки": "change",
    "Удаление заметки": "delete",
    "Выгрузка всех заметок": "get_all",
    "Выгрузка заметок по дате": "get_by_date",
    "Закончить": "exit"
}


def create_note(ident):
    """
    Создание заметки
    """
    print("Введите заголовок заметки:")
    header = input()
    print("Введите тело заметки:")
    message = input()
    return Note(ident, header, message, datetime.now().isoformat())


def change_note(note, data):
    """
    Изменение заметки
    """
    list_data = []
    for noteFromData in data:
        if note == noteFromData:
            list_data.append(note)
        else:
            list_data.append(noteFromData)
    return list_data


def delete_note(note, data):
    """
    Удаление заметки
    """
    list_data = []
    for noteFromData in data:
        if note != noteFromData.ident:
            list_data.append(noteFromData)
    return list_data


def jsonToNote(jsObject):
    """
    Создание сущности Note из json
    """
    return Note(jsObject["ident"], jsObject["header"], jsObject["message"], jsObject["version_date"])


def save_data_to_file(data):
    """
    Сохранение массива заметок в файл
    """
    with open("notes.json", "w") as f:
        json.dump(data, f, cls=NoteEncoder, ensure_ascii=False)


def get_json_from_file():
    """
    Чтение массива заметок из файла
    """
    data = []
    if path.isfile("notes.json") is True:
        with open("notes.json", "r") as f:
            data = json.load(f, object_hook=jsonToNote)
    return data


def add(ident):
    """
    Сохранение новой заметки
    """
    note = create_note(ident)
    data = get_json_from_file()
    data.append(note)
    save_data_to_file(data)
    print("Заметка успешно сохранена")
    return


def get_all():
    """
    Вывод всех заметок на консоль
    """
    for note in get_json_from_file():
        print(note.__dict__)


def change():
    """
    Изменение существующей заметки
    """
    print("Введите идентификатор записи")
    try:
        ident = int(input())
    except:
        print("Идентификатор должен быть числом")
        return
    data_from_file = get_json_from_file()
    for note in data_from_file:
        if ident == note.ident:
            print(note.__dict__)
            new_note = create_note(ident)
            new_data = change_note(new_note, data_from_file)
            save_data_to_file(new_data)
            print("Заметка успешно изменена")
            return
    print(f"Заметки с идентификатором id={ident} не найдено")


def delete():
    """
    Удаление существующей заметки
    """
    print("Введите идентификатор записи, которую хотите удалить")
    ident = int(input())
    data = get_json_from_file()
    for note in data:
        if ident == note.ident:
            print(note.__dict__)
            new_data = delete_note(ident, data)
            save_data_to_file(new_data)
            print("Заметка успешно удалена")
            return
    print(f"Заметки с идентификатором id={ident} не найдено")


def filter_notes(start, end):
    data = get_json_from_file()
    filter_data = []
    for note in data:
        if start <= datetime.strptime(note.version_date, "%Y-%m-%dT%H:%M:%S.%f") <= end:
            filter_data.append(note)
    return filter_data


def get_by_date():
    """
    Получение заметок по дате
    """
    print("Дату и время необходимо вводить в формате yyyy-mm-dd hh:mm:ss")
    print("Введите дату и время, с которого необходимо начать фильтрацию")
    start = input()
    try:
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    except:
        return
    print("Введите дату и время по которое необходимо отфильтровать. Нажмите Enter, если фильтровать по текущую дату")
    end = input()
    try:
        if end == "":
            end = datetime.now()
        else:
            end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    except:
        print("Неверный формат даты или ошибка в дате")
        return
    for note in filter_notes(start, end):
        print(note.__dict__)


def get_command(n):
    if n == command_list["Добавление новой заметки"]:
        add(int(random.uniform(1, sys.maxsize)))
    elif n == command_list["Изменение заметки"]:
        change()
    elif n == command_list["Удаление заметки"]:
        delete()
    elif n == command_list["Выгрузка всех заметок"]:
        get_all()
    elif n == command_list["Выгрузка заметок по дате"]:
        get_by_date()
    elif n == command_list["Закончить"]:
        return


def main():
    print_command_list()
    n = 1
    while n != "exit":
        print("Введите команду:")
        n = input()
        get_command(n)


def print_command_list():
    print("Список доступных команд:")
    for key, value in command_list.items():
        print(key + " -- " + value)


if __name__ == "__main__":
    main()
