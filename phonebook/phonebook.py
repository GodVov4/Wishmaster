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
                print(
                    f"{index + 1}. Ім'я: {contact.name}, Телефон: {contact.phone}, День народження: {contact.birthday}, Пошта: {contact.email}")
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
        today = datetime.now().date()
        interval = timedelta(days=days)
        upcoming = []

        for contact in self.contacts:
            if contact.birthday:
                temporary_birthday = contact.birthday.replace(year=today.year)  # Замінюємо лише рік
                if temporary_birthday <= today + interval:
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
        address_book.load_from_file("saves/address_book.pkl")
    except FileNotFoundError:
        pass

    while True:
        print("-" * 20)
        print("1. Додати контакт")
        print("2. Знайти контакт -> Редагувати / Видалити")
        print("3. Вивести список всіх контактів")
        print("4. Перевірити дні народження")
        print("5. Вийти")

        choice = input("Виберіть дію: ")

        # Додаємо контакт
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
            address_book.save_to_file("saves/address_book.pkl")
            print("Контакт додано!")

        # Шукаємо контакт і вже далі щось з ним робимо
        elif choice == "2":
            search_term = input("Введіть інформацію для пошуку: ")
            search_results = address_book.search_contacts(search_term)
            if search_results:
                print("Знайдені контакти:")
                for index, contact in enumerate(search_results):
                    print(
                        f"{index + 1}. Ім'я: {contact.name}, Телефон: {contact.phone}, "
                        f"День народження: {contact.birthday}, Пошта: {contact.email}")
            else:
                print("Контакти не знайдені.")

            after_search_choice = input("Натисніть: Редагувати - E, Видалити - D, Головне меню - ENTER: ")

            # редагуємо контакт
            if after_search_choice.lower() == "e":
                try:
                    index_to_edit = (int(input("Введіть порядковий номер контакту для редагування: ")) - 1)
                    if 0 <= index_to_edit < len(search_results):

                        contact_to_edit = search_results[
                            index_to_edit]  # Отримуємо контакт для редагування з результатів пошуку
                        new_name = input("Введіть нове ім'я контакту: ")
                        new_phone = input("Введіть новий номер телефону контакту (+380xxxxxxxxx): ")
                        while not is_valid_phone(new_phone):
                            print("Невірний формат номеру телефону! ")
                            new_phone = input("Введіть новий номер телефону контакту (+380xxxxxxxxx): : ")

                        new_birthday = input("Введіть день народження контакту (рік-місяць-день): ")
                        while not is_valid_birthday(new_birthday):
                            print("Невірний формат дня народження!")
                            new_birthday = input("Введіть день народження контакту ще раз (РРРР-ММ-ДД): ")

                        new_email = input("Введіть нову пошту контакту: ")
                        while not is_valid_email(new_email):
                            print("Невірний формат пошти. Введіть ще раз.")
                            new_email = input("Введіть нову пошту контакту: ")

                        # оновлюємо поля контакту
                        contact_to_edit.name = new_name
                        contact_to_edit.phone = new_phone
                        contact_to_edit.birthday = new_birthday
                        contact_to_edit.email = new_email

                        # зберігаємо оновлений список контактів
                        address_book.save_to_file("saves/address_book.pkl")

                        print("Порядковий номер неправильний!")

                except ValueError:
                    print("Неправильний формат вводу!")

            # видаляємо контакт
            elif after_search_choice.lower() == "d":
                try:
                    index_to_delete = int(input("Введіть номер контакту для видалення: ")) - 1
                    if 0 <= index_to_delete < len(search_results):
                        contact_to_delete = search_results[
                            index_to_delete]  # Отримуємо контакт для видалення з результатів пошуку
                        address_book.delete_contact(
                            address_book.contacts.index(contact_to_delete))  # Видаляємо контакт з основного списку

                        # Зберігаємо оновлений список контактів
                        address_book.save_to_file("saves/address_book.pkl")

                    else:
                        print("Номер контакту недійсний.")
                except ValueError:
                    print("Неправильний формат вводу!")


        elif choice == "3":
            address_book.display_all_contacts()


        elif choice == "4":
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

        elif choice == "5":
            print("До побачення!")
            break


if __name__ == "__main__":
    main()
