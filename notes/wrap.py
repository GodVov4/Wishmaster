from note import Notebook


def main():

    notebook = Notebook()

    while True:

        # Виводимо меню з можливими діями
        print("Виберіть дію:")
        print("1 - Створити нотатку")
        print("2 - Редагувати нотатку")
        print("3 - Видалити нотатку")
        print("4 - Пошук по тексту")
        print("5 - Пошук за ключовим словом")
        print("6 - Сортування по даті створення")
        print("7 - Завантажити нотатку")
        print("8 - Вихід з циклу")

        choice = input("Ваш вибір: ")

        if choice == "1":

            text = input("Введіть текст нотатки: ")  # Зчитуємо текст нотатки
            keywords = input("Введіть ключові слова нотатки, розділені комами без пробілів: ").split(
                ",")  # Зчитуємо ключові слова нотатки, розділені комами
            notebook.add_note(text, keywords)  # Додаємо нову нотатку
            print("Нотатку додано")

        elif choice == "2":

            notebook.print_notes()
            # Зчитуємо індекс нотатки для редагування
            try:
                index = int(input("Введіть індекс нотатки для редагування: "))
            except ValueError:
                print('Введіть індекс нотатки')
            # Зчитуємо новий текст нотатки або залишаємо пустим
            text = input("Введіть новий текст нотатки чи залиште пустим: ")
            keywords = input("Введіть нові ключові слова нотатки, розділені комами, чи залиште пустим: ").split(
                ",")  # Зчитуємо нові ключові слова нотатки або залишаємо пустим

            if text or keywords:  # Якщо текст або ключові слова не пусті

                try:
                    # Редагуємо нотатку за індексом
                    notebook.edit_note(index, text, keywords)
                    print("Нотатку відредаговано")
                #  Перехоплюємо помилку з відсутністю нотатки
                except UnboundLocalError:
                    print(
                        'Нотатки з таким індексом не існує. Створіть нову через пункт 1')

            else:
                # Якщо текст і ключові слова пусті, то виводимо повідомлення про помилку
                print("Немає даних для редагування")

        elif choice == "3":

            notebook.print_notes()
            # Зчитуємо індекс нотатки для видалення
            index = int(input("Введіть індекс нотатки для видалення: "))
            notebook.delete_note(index)  # Видаляємо нотатку за індексом

        elif choice == "4":

            # Зчитуємо текст для пошуку
            text = input("Введіть текст для пошуку: ")
            results = notebook.search_by_text(text)  # Пошук нотаток за текстом
            # Виводимо кількість знайдених нотаток
            print(f"Знайдено {len(results)} нотаток:")

            for note in results:  # Проходимо по всіх знайдених нотатках
                print(note)  # Виводимо рядкове представлення нотатки

        elif choice == "5":

            # Зчитуємо ключове слово для пошуку
            keyword = input("Введіть ключове слово для пошуку: ")
            # Пошук нотаток за ключовим словом
            results = notebook.search_by_keyword(keyword)
            # Виводимо кількість знайдених нотаток
            print(f"Знайдено {len(results)} нотаток:")

            for note in results:  # Проходимо по всіх знайдених нотатках
                print(note)

        elif choice == "6":

            reverse = int(
                input("Введіть напрямок сортування (1 - спадання, 0 - зростання): "))
            # Сортуємо список нотаток за датою створення
            notebook.sort_by_date(reverse)
            print("Нотатки відсортовано")

        elif choice == "7":

            filename = input('Введіть назву файлу без розширення ') + ".bin"

            try:
                # Завантажуємо нотатки з файлу
                notebook.load_from_file(filename)

            except FileNotFoundError:
                print('Файл не знайдено. Спробуйте ввести знову')

        elif choice == "8":

            result = input("Зберегти нотатку (y) чи ні(n)? ")
            if result == "y":

                filename = input(
                    "Введіть ім'я файду для збереження нотатки ") + ".bin"
                # Зберігаємо список нотаток у файл
                notebook.save_to_file(filename)
                print("Нотатки збережено")

                break

            else:
                break

        else:
            print("Невірний вибір")


if __name__ == '__main__':
    main()
