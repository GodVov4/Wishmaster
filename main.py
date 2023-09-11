from phonebook.phonebook import main as phonebook_main


def main():
    while True:
        print("-" * 20)
        print("1. Адресна книга")
        print("2. Сортування")
        print("3. Нотатки")
        print("4. Вийти")

        choice = input("Виберіть дію: ")

        if choice == '1':
            # Виклик функціональності з phonebook.py
            phonebook_main()

        # інші варіанти дій тут...

        elif choice == '4':
            break


if __name__ == "__main__":
    main()
