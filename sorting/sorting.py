import os
import shutil
import re
import sys
from tqdm import tqdm


class FileOrganizer:
    def __init__(self, folder):
        self.folder = folder
        self.directories = ['images', 'videos', 'documents', 'audio', 'archives', 'other']
        self.extensions_mapping = {
            'images': ['JPEG', 'JPG', 'PNG', 'SVG'],
            'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
            'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
            'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
            'archives': ['ZIP', 'GZ', 'TAR']
        }
        self.translit_table = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
            'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
            'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }

    def normalize(self, filename):
        filename = filename.translate(str.maketrans(self.translit_table))
        filename = re.sub(r'[^A-Za-z0-9_.]', '_', filename)
        return filename

    def create_directories(self):
        for directory in self.directories:
            os.makedirs(os.path.join(self.folder, directory), exist_ok=True)

    def sort_files(self):
        self.create_directories()

        images = []
        videos = []
        documents = []
        audio = []
        archives = []
        unknown_extensions = []

        # Count total files for progress calculation
        total_files = sum(len(files) for _, _, files in os.walk(self.folder))
        progress_bar = tqdm(total=total_files, desc='Сортування...', unit=' file')

        for root, dirs, files in os.walk(self.folder):
            for file in files:
                file_path = os.path.join(root, file)
                _, extension = os.path.splitext(file)
                new_filename = self.normalize(file)

                destination_folder = None

                extension = extension[1:].upper()
                for directory, extensions in self.extensions_mapping.items():
                    if extension in extensions:
                        destination_folder = directory
                        break
                    else:
                        unknown_extensions.append(new_filename)
                        destination_folder = 'other'

                    if destination_folder:
                        shutil.move(file_path, os.path.join(self.folder, destination_folder, new_filename))

                        if extension in ['ZIP', 'GZ', 'TAR']:
                            shutil.unpack_archive(os.path.join(self.folder, destination_folder, new_filename),
                                                  os.path.join(self.folder, destination_folder))
                            os.remove(os.path.join(self.folder, destination_folder, new_filename))

                    progress_bar.update(1)

            progress_bar.close()

            for root, dirs, files in os.walk(self.folder, topdown=False):
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)

            return images, videos, documents, audio, archives, unknown_extensions


def main():
    folder = input("Введіть шлях до теки для організації: ")

    if not os.path.isdir(folder):
        print('Невірний шлях до теки. Вихід...')
        sys.exit(1)

    print(f'Організація файлів у теці: {folder}')

    organizer = FileOrganizer(folder)

    images, videos, documents, audio, archives, unknown_extensions = organizer.sort_files()

    print('Сортування завершено.')


if __name__ == '__main__':
    main()
