import pickle
from phonebook.phonebook import Contact, AddressBook


def main():
    address_book = AddressBook()

    try:
        address_book.load_from_file('address_book.pkl')
    except FileNotFoundError:
        pass

    while True:
        print("1. Додати контакт")
        print("2. Знайти контакт")
        print("3. Вивести список всіх контактів")
        print("4. Вийти")

        choice = input("Виберіть дію: ")

        if choice == '1':
            name = input("Введіть ім'я контакту: ")
            phone = input("Введіть номер телефону контакту: ")
            contact = Contact(name, phone)
            address_book.add_contact(contact)
            address_book.save_to_file('address_book.pkl')
            print("Контакт додано!")


        elif choice == '2':
            search_term = input("Введіть рядок для пошуку: ")
            results = address_book.search_contacts(search_term)
            if results:
                print("Знайдені контакти:")
                for contact in results:
                    print(f"Ім'я: {contact.name}, Телефон: {contact.phone}")
            else:
                print("Контакти не знайдені.")

        elif choice == '3':
            address_book.display_all_contacts()

        elif choice == '4':
            break


if __name__ == "__main__":
    main()
