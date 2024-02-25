from typing import List
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value: str):
        if not value:
            raise ValueError
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        if not value.strip():
            raise ValueError
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name: Name):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Birthday = None

    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break
        else:
            raise ValueError("Phone number not found.")

    def __str__(self):
        phone_numbers = '; '.join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_numbers}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_week = today + timedelta(days=7)
        return [record for record in self.data.values() if record.birthday and today <= datetime.strptime(record.birthday.value, "%d.%m.%Y").date() < upcoming_week]


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").split()
        command, args = user_input[0], user_input[1:]

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")

        if command == "add":
            if len(args) != 2:
                print("Invalid format. Please use: add [name] [phone]")
            else:
                name, phone = args
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print("Contact added.")

        if command == "change":
            if len(args) != 3:
                print("Invalid format. Please use: change [name] [old phone] [new phone]")
            else:
                name, old_phone, new_phone = args
                record = book.find(name)
                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print("Phone number updated.")
                    except ValueError as e:
                        print(e)
                else:
                    print("Contact not found.")

        if command == "phone":
            if len(args) != 1:
                print("Invalid format. Please use: phone [name]")
            else:
                name = args[0]
                record = book.find(name)
                if record:
                    print(record)
                else:
                    print("Contact not found.")

        if command == "add-birthday":
            if len(args) != 2:
                print("Invalid format. Please use: add-birthday [name] [birthday (DD.MM.YYYY)]")
            else:
                name, birthday = args
                record = book.find(name)
                if record:
                    try:
                        record.add_birthday(birthday)
                        print("Birthday added.")
                    except ValueError as e:
                        print(e)
                else:
                    print("Contact not found.")

        if command == "birthdays":
            upcoming_birthdays = book.get_upcoming_birthdays()
            if not upcoming_birthdays:
                print("No upcoming birthdays in the next week.")
            else:
                print("Upcoming birthdays:")
                for record in upcoming_birthdays:
                    print(f"{record.name.value}'s birthday is on {record.birthday.value}.")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
'''
Enter a command: add John 1234567890
Contact added.
Enter a command: add Jane 9876a12345
Invalid format. Please use: add [name] [phone]
Enter a command: add Jane
Invalid format. Please use: add [name] [phone]
Enter a command: change Michael 1234567890 9876543210
Contact not found.
Enter a command: phone Michael
Contact not found.
Enter a command: add-birthday John 1990-12-25
Invalid date format. Use DD.MM.YYYY
Enter a command: add-birthday John 25.12.1990
Birthday added.
Enter a command: birthdays
Upcoming birthdays:
John's birthday is on 25.12.1990.
Enter a command: close
Good bye
'''