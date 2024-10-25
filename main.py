import os
import json

open_name_file = ''
current_contact = {}

def info():
    global open_name_file
    if open_name_file == '':
        return "!!! Нет открытого файла контактов"
    else:
        return 'Загружен файл ' + open_name_file

def error_open_data():
    print()
    print('!!!  Нет открытой базы ')
    print()

def load_data(name_file):
    global current_contact
    with open('./data_contacts/' + name_file, 'r', encoding='utf-8') as file:
        current_contact.update(json.load(file))

def save_data(name_file, data):
    path = './data_contacts/' + name_file
    with  open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# печатаем таблицу с контактами
def print_contact(data_contact):
    #print('>>>>>', len(data_contact))
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
    print('=' * (max_len_name + max_len_last + max_len_phone + 10))
    for index, item in enumerate(data_contact):
        if item['name'] == '':
            continue
        print(f'{index+1:3} | {item['name']:{max_len_name +3}} | {item['last_name']:{max_len_last + 4}}| {item['phone']:{max_len_phone + 2}}')
    print()



# загружаем имя файла в глобальную переменную
def open_data_base():
    if os.path.isdir('./data_contacts'):
        print('Список баз контактов')
        print('-' * 30)
        data = os.listdir('./data_contacts')
        i = 1
        for el in data:
            print(f'{i}. {el}')
            i += 1
        print('=' * 30)
        is_num = True
        while is_num:
            nomer_file = input('Введите номер файла или -1 для выхода >>> ')
            #print(nomer_file)
            if nomer_file.isdigit() and ( 1 <= int(nomer_file) <= len(data) ):
                is_num = False
                global open_name_file
                open_name_file = data[int(nomer_file) - 1]
                print()
                load_data(open_name_file)
            elif nomer_file == '-1':
                is_num = False


# создает новый файл json и присваивает имя к глобальной переменой
def new_data_base():
    name_file = input('Введите название базы контактов или -1 для выхода>>> ')

    if name_file != '-1':
        file_exists = True
        while file_exists:
            if (name_file + '.json' )in os.listdir('./data_contacts'):
                name_file = input('!!! Файл существует введите другое название >>> ')
            else:
                file_exists = False
                with open('./data_contacts/' + name_file + '.json', 'w', encoding='utf-8') as f:
                    json.dump({'data':[]}, f)
        global open_name_file
        open_name_file = name_file + '.json'

# красивое меню :)
def print_menu():
    print()
    print('-' * 40)
    print('| Добро пожаловать в телефонную книгу. |')
    print('-' * 40)
    print('1.  Открыть базы контактов ')
    print('2.  Создать базу контактов')
    print('3.  Поиск контакта по номеру телефона') # попозже
    print('    или по  Имени или Фамилии') # попозже
    print('4.  Добавить контакт')
    print('5.  Удалить контакт')
    print('6.  Показать список контактов')
    print('7.  Помощь')
    print('8.  Выйти')
    print()
    print(info())
    print()
    return input('Введите номер пункта меню >>> ')

# добавление контакта
def add_contact():
    global open_name_file
    global current_contact
    if open_name_file != '':
        dobavit_new_contact = True
        load_data(open_name_file)
        while dobavit_new_contact:
            name = input('    Введите имя >>> ')
            last_name = input('Введите Фамилию >>> ')
            phones = input('Введите номер телефона >>> ')
            print('=' * 30)
            print('* Добавить еще контакт нажмите любую символ')
            print('* Для выхода нажмите клавишу < 2 > ')
            nomer_punkt = input('Введите номер команды >>> ')
            if nomer_punkt == '2':
                dobavit_new_contact = False
            current_contact['data'].append({'name': name, 'last_name': last_name, 'phone': phones})
    else:
        error_open_data()
        open_data_base()
        add_contact()
    save_data(open_name_file, current_contact)

def delete_contact():
    f_del = True
    while f_del:
        if open_name_file != '':
            print_contact(current_contact['data'])
            delete_items = input('Введите номер контакта для удаления или N для отмены >>> ')
            if not(delete_items in ['N', 'n', 'т', 'Т']):
                delete_items =  int(delete_items if delete_items.isdigit() and delete_items != '' else '-1')
                if delete_items != -1 and delete_items <= len(current_contact['data']):
                    del_i = current_contact['data'].pop(delete_items - 1)
                    save_data(open_name_file, current_contact)
                    print(f'Удален контакт {del_i['name']}  {del_i['last_name']}  {del_i['phone']}')
                    print()
        else:
            error_open_data()
            open_data_base()
            delete_contact()
        res = input(' Продолжить удаление контакта Y - да, N - выход >>> ')
        if res.strip() in ['N', 'n', 'т', 'Т']:
            f_del = False

def search(what_s):
    """
    :param what_s: кого мы ищем,
    :return:
    """
    if open_name_file != '':
        print(f'Результат поиска: {what_s}')
        res = []
        for item in current_contact['data']:
            if what_s == item['name'] or what_s == item['last_name' or what_s == item['phone']]:
                res.append(item)
        #print(res)
        if res:
            print()
            print_contact(res)
            print()
        else:
            print()
            print('Нет совпадений !!!')
            print()
            #input('Нажмите любую клавишу для продолжения ....')
    else:
        error_open_data()
        open_data_base()
        search(what_s)

def menu_poisk():
    poisk_bul = True
    while poisk_bul:
        poisk = input('Введите Имя, Фамилию или № телефона для поиска: ')
        search( poisk)
        prodoljit = input('Продолжить поиск Y - да, N - выход >>> ')
        if prodoljit.strip() in ['N', 'n', 'т', 'Т']:
            poisk_bul = False

def list_contacts():
    global open_name_file
    if open_name_file == '':
        error_open_data()
        open_data_base()
        print_contact(current_contact['data'])

    else:
        print_contact(current_contact['data'])

exit = True
nomer_menu = print_menu()

while exit:
    if nomer_menu == '1':
        open_data_base()
        #print(open_name_file)
        nomer_menu = print_menu()

    elif nomer_menu == '2':
        new_data_base()
        nomer_menu = print_menu()

    elif nomer_menu == '3':
        menu_poisk()
        nomer_menu = print_menu()

    elif nomer_menu == '4':
        add_contact()
        nomer_menu = print_menu()

    elif nomer_menu == '5':
        delete_contact()
        nomer_menu = print_menu()

    elif nomer_menu == '6':
        list_contacts()
        input('Для продолжения нажмите любую клавишу...')
        nomer_menu = print_menu()

    elif nomer_menu == '7':
        print('HELP')
        nomer_menu = print_menu()

    elif nomer_menu == '8':
        exit = False
    else:
        print()
        print('  !!! Неправильный номер меню, выбирите из списка ')
        nomer_menu = print_menu()
