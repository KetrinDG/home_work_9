import click
import json

# ошибка ввода
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return """If you write command 'add' please write 'add name number'\nIf you write command 'change' please write 'change name number'\nIf you write command 'phone' please write 'phone name'"""
        except KeyError:
            return "..."

    return wrapper

#отсутствует файл
def read_file():
    try:
        with open("contacts.txt", "r", encoding="UTF-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@input_error
def add_help():
    return """help - output command, that help find command\nhello - output command 'How can I help you?'\nadd - add contact, use 'add' 'name' 'number'\nchange - change your contact, use 'change' 'name' 'number'\nphone - use 'phone' 'name' that see number this contact\nshow all - show all your contacts"""

@input_error
def add_bye(*args):
    return "Good bye, see you soon"

@input_error
def add_hello(*args):
    return "How can I help You?\nIf you want to know what I can do write Help "

#работа с текстом

def write_file(contacts):
    with open('contacts.txt', 'w', encoding='UTF-8') as file:
        json.dump(contacts, file)

#создание контакта
@input_error
def add_add(*args):
    name = args[0]
    number = args[1]
    contacts = read_file()
    if contacts.get(args[0]):
        return 'This contact already exist'
    else:
        contacts.update({name: number})
    write_file(contacts)
    return f'Contact "{name}" add successfully'

#изменение контакта
@input_error
def add_change(*args):
    name = args[0]
    number = args[1]
    contacts = read_file()
    if contacts.get(name):
        contacts.update({name: number})
    else:
        return f'No contact "{name}"'
    write_file(contacts)
    return f"Contact '{name}' change successfully"

@input_error
def add_phone(*args):
    name = args[0]
    contacts = read_file()
    if contacts.get(name):
        return '\t{:>20} : {:<12} '.format(name, contacts.get(name))
    else:
        return f'No contact "{name}"'

#отобразить все
def add_show(*args):
    contacts = read_file()
    result = []
    for name, numbers in contacts.items():
        result.append('\t{:>20} : {:<12} '.format(name, numbers))
    return '\n'.join(result)

#работа по командам
commands = {
    add_hello: "hello",
    add_add: "add",
    add_phone: "phone",
    add_show: "show all",
    add_change: "change",
    add_bye: "good bye",
    add_help: "help"
    }

def command_parser(user_input):
    data = []
    command = ""
    for k, v in commands.items():
        if user_input.lower().startswith(v):
            command = k
            data = user_input.replace(v, "").split()
    return command, data

def start_hello():
    return f"Hello, I'm a bot assistent.\nTo get started, write Hello"

@click.command()
def main():

    #начало программы
    while True:
        user_input = input(">>> ")
        command, data = command_parser(user_input)
        if command:
            print(command(*data))
            if command == add_bye:
                break
        else:
            print("Sorry, unknown command. Try again.")


if __name__ == "__main__":
    print(start_hello())
    main()