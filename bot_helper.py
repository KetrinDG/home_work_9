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


# отсутствует файл
def read_file():
    try:
        with open("contacts.txt", "r", encoding="UTF-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@input_error
def help_command():
    help_list = [
        "help - output command, that help find command",
        'hello - output command "How can I help you?"',
        'add - add contact, use "add" "name" "number"',
        'change - change your contact, use "change" "name" "number"',
        'phone - use "phone" "name" that see number this contact',
        "show all - show all your contacts",
    ]
    return "\n".join(help_list)


@input_error
def bye_command(*args):
    return "Good bye, see you soon"


@input_error
def hello_command(*args):
    return "How can I help You?\nIf you want to know what I can do write Help "


# работа с текстом


def write_file(contacts):
    with open("contacts.txt", "w", encoding="UTF-8") as file:
        json.dump(contacts, file)


# создание контакта
@input_error
def add_command(*args):
    name = args[0]
    number = args[1]
    contacts = read_file()
    if contacts.get(args[0]):
        return "This contact already exist"
    else:
        contacts.update({name: number})
    write_file(contacts)
    return f'Contact "{name}" add successfully'


# изменение контакта
@input_error
def change_command(*args):
    name = args[0]
    number = args[1]
    contacts = read_file()
    if contacts.get(name):
        # contacts.update({name: number})
        contacts[name] = number  # тут все одно ми вже знаємо, що контакт існує)
    else:
        return f'No contact "{name}"'
    write_file(contacts)
    return f"Contact '{name}' change successfully"


@input_error
def add_phone_command(*args):
    name = args[0]
    contacts = read_file()
    if contacts.get(name):
        return "\t{:>20} : {:<12} ".format(name, contacts.get(name))
    else:
        return f'No contact "{name}"'


# отобразить все
def show_all(*args):
    contacts = read_file()
    result = []
    for name, numbers in contacts.items():
        result.append("\t{:>20} : {:<12} ".format(name, numbers))
    return "\n".join(result)


# работа по командам
commands = {
    hello_command: ["hello"],
    add_command: ["add"],
    add_phone_command: ["phone"],
    show_all: ["show all"],
    change_command: ["change"],
    bye_command: ["good bye", "bye", "."],
    help_command: ["help"],
}


def command_parser(user_input):
    data = []
    command = ""
    for k, v in commands.items():
        if any([user_input.lower().startswith(i) for i in v]):
            command = k
            data = " ".join([user_input.replace(i, "") for i in v]).split()
    return command, data


def start_hello():
    return f"Hello, I'm a bot assistent.\nTo get started, write Hello"


@click.command()
def main():
    # начало программы
    while True:
        user_input = input(">>> ")
        command, data = command_parser(user_input)
        if command:
            print(command(*data))
            if command == bye_command:
                break
        else:
            print("Sorry, unknown command. Try again.")


if __name__ == "__main__":
    print(start_hello())
    main()
