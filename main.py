import json
from pathlib import Path


def save_data(path:str, data: dict):
    """
    Сохраняет данные контактов в файл
    :param path: относительный путь
    :param data: данные для сохранения
    :return:
    """
    path_data = Path(path)
    with  path_data.open('w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_data(path: str) -> dict[str]:
    """
    Загружает файл с контактами
    :param path: путь до файла
    :return: Словарь контактов
    """
    p = Path(path)
    with p.open('r', encoding='UTF-8') as file:
        content = json.load(file)
    return content


def file_exists(data_path:list[str], name_file: str) -> str:
    """
    Возвращает True если файл существует, иначе False

    :param data_path: список путей
    :param name_file: имя файла
    :return: возвращает путь до файла если оно существует иначе пустую строку
    """
    for path in data_path:
        if name_file in path:
            return path
    return ''


def name_path_file(path: str) -> str:
    """
    возвращает имя файла из относительного пути
    :param path: путь до файла относительно скрипта
    :return: имя файла с расширением
    """
    return path[14:]


def files_menu(list_filles: list[str]) -> str:
    """
    Показывает меню выбора файла
    :param list_filles: список путей файлов
    :return: возвращает путь выбранного файла
    """
    print()
    i = 1
    for item in list_filles:
        print(f' {i}  {name_path_file(item)}')
        i += 1
    n = input('Введите номер файла для открытия: ')
    if n.isdigit() and int(n) <= len(list_filles):
        return list_filles[int(n)-1]
    return ''


def new_data_base():
    """
    Создает новый файл с базами json
    :return: возвращает путь с новым именем файла
    """
    flag = True
    while flag:
        name_file = input(' Введите имя файла без расширения: ')
        if not file_exists(list_files(), name_file + '.json'):
            flag = False
            return './data_contacts' + '/' + name_file + '.json'
        else:
            print()
            print(' !!! Файл существует измените имя файла ')




def print_menu() -> str:
    """
    Главное меню
    :return: номер (строка)
    """
    print()
    print('-' * 40)
    print(' | Добро пожаловать в телефонную книгу. |')
    print('-' * 40)
    print(' 1.  Открыть базы контактов ')
    print(' 2.  Создать базу контактов')
    print(' 3.  Поиск контакта по номеру телефона') # попозже
    print('     или по  Имени или Фамилии') # попозже
    print(' 4.  Добавить контакт')
    print(' 5.  Удалить контакт')
    print(' 6.  Показать список контактов')
    print(' 7.  Изменить контакт')
    print(' 8.  Помощь')
    print(' 9.  Выйти')
    print()
    return input(' Введите номер пункта меню >>> ')


def list_files() -> list:
    """
    Парсит папку и возвращает все относительные пути до файлов
    :return: Возвращает список путей файлов
    """
    path_data = Path('./data_contacts').glob('*.json')
    return list(map(str, path_data))


def print_contact(data_contact:list):
    """
    Печатает на экране список контактов
    :param data_contact: список контактов
    :return: None
    """
    #максимальная ширина колонок
    max_len_name = 0
    max_len_last = 0
    max_len_phone = 0
    #print(data_contact)
    for item in data_contact:
        #print(item)
        len_name = len(item['name'])
        len_last_n = len(item['last_name'])
        len_phone = len(item['phone'])
        max_len_name = max(max_len_name, len_name)
        max_len_last = max(max_len_last, len_last_n)
        max_len_phone = max(max_len_phone, len_phone)
    #print(max_len_name, max_len_last, max_len_phone)
    # Печать шапки
    nam = 'Имя'
    las = 'Фамилие'
    phon = 'Телефон'
    print(f' №  | {nam:{max_len_name +3}} | {las:{max_len_last + 4}}| {phon:{max_len_phone + 2}}')
    print('=' * (max_len_name + max_len_last + max_len_phone + 18))
    for index, item in enumerate(data_contact):
        if item['name'] == '':
            continue
        print(f'{index+1:3} | {item['name']:{max_len_name +3}} | {item['last_name']:{max_len_last + 4}}| {item['phone']:{max_len_phone + 2}}')
    print()


def search(data: dict, what_s: str):
    """
    Поиск по Имени Фамилии или номеру телефона
    :param data: база контактов
    :param what_s: кого мы ищем
    :return: None
    """
    print(f' Результат поиска: {what_s}')
    res = []
    for item in data['data']:
        if what_s.strip() == item['name'] or what_s.strip() == item['last_name'] or what_s.strip() == item['phone']:
            res.append(item)
        #print(res)

    if res:
        print()
        print_contact(res)
        print()
    else:
        print()
        print(' Нет совпадений !!!')
        print()


def menu_poisk(data:dict):
    """
    Меню поиска
    :param data: словарь контактов
    :return:  None
    """
    if data:
        poisk_bul = True
        while poisk_bul:
            poisk = input(' Введите Имя, Фамилию или № телефона для поиска: ')
            search(data, poisk)
            prodoljit = input(' Продолжить поиск Y - да, N - выход >>> ')
            if prodoljit.strip() in ['N', 'n', 'т', 'Т']:
                poisk_bul = False
    else:
        print()
        print(' !!! Нет открытой базы контактов')


def add_contact(path:str, data: dict[str]) -> dict[str]:
    """
    Добавляет контакт в словарь
    :param path: путь до файла
    :param data: словарь контактов
    :return: словарь с добавленным контактом
    """
    if path != '':
        dobavit_new_contact = True
        while dobavit_new_contact:
            name = input('     Введите имя >>> ')
            last_name = input(' Введите Фамилию >>> ')
            phones = input(' Введите номер телефона >>> ')
            print(' =' * 30)
            print(' * Добавить еще контакт нажмите любую символ')
            print(' * Для выхода нажмите клавишу < 2 > ')
            nomer_punkt = input('Введите номер команды >>> ')
            if nomer_punkt == '2':
                dobavit_new_contact = False
            data['data'].append({'name': name, 'last_name': last_name, 'phone': phones})
    else:
        print()
        print(' !!! Не открыта база контактов')
    return data


def delete_contact(path:str, data_contacts:dict[str]) -> dict[str]:
    """
    Удаляет контакт
    :param path: путь до файла
    :param data_contacts: контакты
    :return: возвращает словарь с удаленным элементом
    """
    f_del = True
    while f_del:
        no_open_contact = False
        if path != '':
            print_contact(data_contacts['data'])
            delete_items = input(' Введите номер контакта для удаления или N для отмены >>> ')
            if not(delete_items in ['N', 'n', 'т', 'Т']):
                delete_items =  int(delete_items if delete_items.isdigit() and delete_items != '' else '-1')
                if delete_items != -1 and delete_items <= len(data_contacts['data']):
                    del_i = data_contacts['data'].pop(delete_items - 1)
                    print(f' Удален контакт {del_i['name']}  {del_i['last_name']}  {del_i['phone']}')
                    print()
        else:
            print()
            print(' !!! Нет отрытой базы контактов')
            no_open_contact = True
            f_del = False
        if not no_open_contact:
            res = input('  Продолжить удаление контакта Y - да, N - выход >>> ')
            if res.strip() in ['N', 'n', 'т', 'Т']:
                f_del = False
    return data_contacts


def help():
    help = """
              Учебная программа 'Телефонный справочник.'
    
    Программа телефонный справочник, умеет сохранять, открывать, искать, удалять контакты.
    Интерфейс текстовый. Для хранения контактов используется JSON файл. Для разделения по
    категориям ИСПОЛЬЗУЙТЕ ИМЯ файла. 
    
    """
    print(help)


def change_help(data: str, t: str) -> str:
    """
    Вспомогательная ф-я меню для изменения контакта
    :param data: данные для изменения
    :param t: имя атрибута (Имя, фамилия, телефон)
    :return: возвращает старое значение или новую
    """
    comm = input(f' Изменить {t} {data} Y - да, N - оставить: ')
    if comm in ['N', 'n', 'т', 'Т']:
        return data
    else:
        inp = input(f' Введите новое {t}: ')
        return inp


def change_contact(data_contacts:dict[str]) -> dict[str]:
    """
    Изменяет контакт
    :param data_contacts: список контактов
    :return: новый список контактов
    """
    if data_contacts:
        print_contact(data_contacts['data'])
        ren_item = input(' Введите номер для изменения: ')
        int_ren_items = int(ren_item if ren_item.isdigit() and ren_item != '' else '-1')
        if int_ren_items != -1 and int_ren_items <= len(data_contacts['data']):
            reneim= data_contacts['data'].pop(int_ren_items - 1)
            name = change_help(reneim['name'], 'Имя')
            l_name = change_help(reneim['last_name'], 'Фамилию')
            r_phone = change_help(reneim['phone'], 'телефон')
            data_contacts['data'].append({'name': name, 'last_name': l_name, 'phone': r_phone})
            return data_contacts
    else:
        print()
        print(' !!! Не загружена база контактов')


def main():
    current_file_path = ''
    exit = True
    current_contact = {}

    nomer_menu = print_menu()
    while exit:
        if nomer_menu == '1':
            if current_file_path:
                save_data(current_file_path, current_contact)
            # Открыть базы контактов
            current_file_path = files_menu(list_files())
            current_contact = load_data(current_file_path)
            flag_load_data = True
            nomer_menu = print_menu()

        elif nomer_menu == '2':
            # Создать базу контактов
            if current_file_path:
                save_data(current_file_path, current_contact)
            current_contact = {'data': []}
            current_file_path = new_data_base()
            print(current_file_path)
            nomer_menu = print_menu()

        elif nomer_menu == '3':
            # Поиск контакта по номеру телефона
            menu_poisk(current_contact)
            nomer_menu = print_menu()

        elif nomer_menu == '4':
            # Добавить контакт
            current_contact = add_contact(current_file_path, current_contact)
            nomer_menu = print_menu()

        elif nomer_menu == '5':
            # Удалить контакт
            current_contact = delete_contact(current_file_path, current_contact)
            nomer_menu = print_menu()

        elif nomer_menu == '6':
            # Показать список контактов
            if current_contact:
                print_contact(current_contact['data'])
            else:
                print()
                print('!!! Нет отрытой базы контактов')
            input(' Для продолжения нажмите любую клавишу...')
            nomer_menu = print_menu()

        elif nomer_menu == '7':
            current_contact = change_contact(current_contact)
            nomer_menu = print_menu()

        elif nomer_menu == '8':
            help()
            nomer_menu = print_menu()

        elif nomer_menu == '9':
            # Сохранить базу контактов
            if current_file_path:
                y_n = input(' !!! База не сохранена, сохранить <Y, N> <Д/Н>: ')
                if y_n.strip() in ['Y', 'y', 'Д', 'д']:
                    save_data(current_file_path, current_contact)
            exit = False

        else:
            print()
            print('   !!! Неправильный номер меню, выбирите из списка ')
            nomer_menu = print_menu()


if __name__ == '__main__':
    main()
