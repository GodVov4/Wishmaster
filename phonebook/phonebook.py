import pickle
import re
from datetime import datetime, timedelta


class Contact:
    def __init__(self, name, phone, birthday, email):
        self.name = name
        self.phone = phone
        self.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()  # одразу переводжу ДН в обʼєкт datetime
        self.email = email


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, "rb") as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            pass

    def search_contacts(self, search_term):
        results = []
        for contact in self.contacts:
            if (search_term.lower() in contact.name.lower()) or (search_term in contact.phone):
                results.append(contact)
        return results

    def display_all_contacts(self):
        if self.contacts:
            print("Список користувачів:")
            for index, contact in enumerate(self.contacts):
                print(f"{index + 1}. Ім'я: {contact.name}, Телефон: {contact.phone}, День народження: {contact.birthday}, Пошта: {contact.email}")
        else:
            print("Адресна книга порожня.")

    def edit_contact(self, index, name, phone, birthday, email):
        if 0 <= index < len(self.contacts):
            self.contacts[index].name = name
            self.contacts[index].phone = phone
            self.contacts[index].birthday = birthday
            self.contacts[index].email = email
            self.save_to_file("address_book.pkl")
            print("Контакт відредаговано!")

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            deleted_contact = self.contacts.pop(index)
            self.save_to_file("address_book.pkl")
            print(f"Контакт {deleted_contact.name} видалено!")

    def upcoming_birthdays(self, days):
        today = datetime.now()
        interval = timedelta(days=days)
        upcoming = []

        for contact in self.contacts:
            if contact.birthday:
                temporary_birthday = contact.birthday.replace(year=today.year)
                if temporary_birthday <= today.date() + interval:
                    upcoming.append(contact)

        return upcoming


# Перевірка правильності формату номеру телефону
def is_valid_phone(phone):
    return bool(re.match(r"^\+380\d{9}$", phone))

# Перевірка правильності формату дня народження (дати)
def is_valid_birthday(birthday):
    return bool(re.match(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$", birthday))

# Перевірка правильності формату пошти
def is_valid_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


# Основна частина програми
def main():
    address_book = AddressBook()

    try:
        address_book.load_from_file("address_book.pkl")
    except FileNotFoundError:
        pass

    while True:
        print("-" * 20)
        print("1. Додати контакт")
        print("2. Знайти контакт")
        print("3. Вивести список всіх контактів")
        print("4. Редагувати контакт")  # це пропоную перенести в 2. Знайти контакт
        print("5. Видалити контакт")  # це теж можна в 2
        print("6. Перевірити дні народження")
        print("7. Вийти")

        choice = input("Виберіть дію: ")

        if choice == "1":
            name = input("Введіть ім'я контакту: ")
            
            phone = input("Введіть номер телефону контакту (+380xxxxxxxxx): ")
            while not is_valid_phone(phone):
                print("Невірний формат номеру телефону. Введіть ще раз (+380xxxxxxxxx): ")
                phone = input("Введіть номер телефону контакту: ")

            birthday = input("Введіть день народження контакту (рік-місяць-день): ")
            while not is_valid_birthday(birthday):
                print("Невірний формат дня народження!")
                birthday = input("Введіть день народження контакту ще раз (РРРР-ММ-ДД): ")
            
            email = input("Введіть пошту контакту: ")
            while not is_valid_email(email):
                print("Невірний формат пошти. Введіть ще раз.")
                email = input("Введіть пошту контакту: ")

            contact = Contact(name, phone, birthday, email)
            address_book.add_contact(contact)
            address_book.save_to_file("address_book.pkl")
            print("Контакт додано!")

        elif choice == "2":
            search_term = input("Введіть інформацію для пошуку: ")
            search_results = address_book.search_contacts(search_term)
            if search_results:
                print("Знайдені контакти:")
                for index, contact in enumerate(search_results):
                    print(f"{index + 1}. Ім'я: {contact.name}, Телефон: {contact.phone}, День народження: {contact.birthday}, Пошта: {contact.email}")
            else:
                print("Контакти не знайдені.")

        elif choice == "3":
            address_book.display_all_contacts()

        elif choice == "4":
            try:
                index = (int(input("Введіть номер контакту для редагування: ")) - 1)  # це треба покласти аргументом в метод search_contact
                if 0 <= index < len(address_book.contacts):
                    name = input("Введіть нове ім'я контакту: ")
                    phone = input("Введіть новий номер телефону контакту (+380xxxxxxxxx): ")
                    while not is_valid_phone(phone):
                        print("Невірний формат номеру телефону. Введіть ще раз (+380xxxxxxxxx): ")
                        phone = input("Введіть новий номер телефону контакту: ")
                    
                    birthday = input("Введіть день народження контакту (рік-місяць-день): ")
                    while not is_valid_birthday(birthday):
                        print("Невірний формат дня народження!")
                        birthday = input("Введіть день народження контакту ще раз (РРРР-ММ-ДД): ")

                    email = input("Введіть нову пошту контакту: ")
                    while not is_valid_email(email):
                        print("Невірний формат пошти. Введіть ще раз.")
                        email = input("Введіть нову пошту контакту: ")
                    address_book.edit_contact(index, name, phone, birthday, email)
                else:
                    print("Номер контакту недійсний.")
            except ValueError:
                print("Неправильний формат вводу!")

        elif choice == "5":
            try:
                index = int(input("Введіть номер контакту для видалення: ")) - 1
                if 0 <= index < len(address_book.contacts):
                    address_book.delete_contact(index)
                else:
                    print("Номер контакту недійсний.")
            except ValueError:
                print("Неправильний формат вводу!")

        elif choice == "6":
            try:
                days = int(input("Який проміжок часу перевірити? (введіть число днів): "))
            except ValueError:
                print("Неправильний формат вводу!")
                continue  # Перейти на наступну ітерацію циклу

            upcoming = address_book.upcoming_birthdays(days)
            if upcoming:
                print(f"Контакти з днями народження, які настають протягом наступних {days} днів:")
                for contact in upcoming:
                    print(f"Ім'я: {contact.name}, День народження: {contact.birthday}")
            else:
                print("Немає контактів з наближеними днями народження.")

        elif choice == "7":
            print("До побачення!")
            break


if __name__ == "__main__":
    main()

"""
Якраз в них має бути валідація полів перед записом. Тільки проперті можеш закинути в Field, щоб не було повторень, а setter викликатиметься через @Field.value.setter
Також перепиши ініт з того скріна
"""
