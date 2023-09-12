import argparse
import re
import sys
from pathlib import Path
from shutil import copyfile
""" 

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help = 'sorter_folder')
parser.add_argument('--output', '-o', default='dist', help = 'sorted_folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')

def read_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            read_folder(el)
        else:
            copy_file(el)


def copy_file(file: Path) -> None:
    ext = file.suffix
    new_path = output_folder / ext
    new_path.mkdir(exist_ok=True, parents=True)
    copyfile(file, new_path / file.name)


output_folder = Path(output)
read_folder(Path(source))

cyrillic_sumbols = 'абвгдеєжзиіїйклмнопрстуфцчшщьюя'
latinic_sumbols = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'yo', 'ya')

TRANS = {}
for a, b in zip(cyrillic_sumbols, latinic_sumbols):
    TRANS[ord(a)] = b
    TRANS[ord(a.upper)] = b.upper

def normalize(name: str) -> str:
    n_name = name.translate(TRANS)
    n_name = re.sub(r'\w', '_', n_name)
    return n_name """

IMAGES = []
MUSIC = []
VIDEO = []
DOCUMENTS = []
ARCHIVES = []
MY_OTHERS = []


FOLDERS = []
EXTENSION = set()
UNKNOWS = set() 
REGISTER_EXTENTIONS = {} 
    
class Field():
    def __init__(self, value, file):   
        self.value = value 
        self.file = file


class Images(Field):
    pass

class Music(Field):
    pass

class Video(Field):
    pass

class Documents(Field):
    pass 

class Archives(Field):
    pass 
class My_other(Field):
    pass 



class Sorter():
    
    def __init__(self, file, filename, fullname, IMAGES = Images, VIDEO = Video, DOCUMENTS = Documents, MUSIC = Music, ARCHIVES = Archives):
        self.file = file
        self.filename = filename
        self.fullname = fullname
        self.IMAGES = IMAGES
        self.VIDEO = VIDEO
        self.DOCUMENTS = DOCUMENTS
        self.MUSIC = MUSIC
        self.ARCHIVES = ARCHIVES
    
    REGISTER_EXTENTIONS = {
        "jpg":IMAGES,
        'png': IMAGES,
        'svg': IMAGES,
        'avi': VIDEO,
        'mp4': VIDEO,
        'mov': VIDEO,
        'mkv': VIDEO,
        'doc': DOCUMENTS,
        'txt': DOCUMENTS,
        'pdf': DOCUMENTS,
        'mp3': MUSIC,
        'wav': MUSIC,
        'arm': MUSIC,
        'zip': ARCHIVES,
        'gz':  ARCHIVES,
        'tar': ARCHIVES}
    
    


    def get_extention(filename: str) -> str:
        return Path(filename). suffix[1:]. lower()

    def scan(folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'images', 'audio', 'video', 'documents', 'MY_OTHERS'):
                    FOLDERS.append(item)
                    #scan(item)
                continue

            ext = get_extention(item.name)
            fullname = folder / item.name 
            if not ext:
                MY_OTHERS.append(fullname)
            
            # #else:
            #     container = REGISTER_EXTENTIONS[ext]    
            #     EXTENSION.add(ext)
            #     container.append(fullname)
            
            if item.is_file():
                if item.name.endswith('.jpg') or item.name.endswith('.png') or item.name.endswith('.svg') :
                    IMAGES.append(fullname)
                if item.name.endswith('.avi') or item.name.endswith('mp4')  or item.name.endswith('mov') or item.name.endswith('mkv') :
                    VIDEO.append(fullname)
                if item.name.endswith('.doc') or item.name.endswith('txt')   or item.name.endswith('pdf') :
                    DOCUMENTS.append(fullname)
                if item.name.endswith('.mp3') or item.name.endswith('wav')  or item.name.endswith('arm') :
                    MUSIC.append(fullname)
                if item.name.endswith('zip') or item.name.endswith('gz')  or item.name.endswith('tar') :
                    ARCHIVES.append(fullname)
                    
                
                
                
                
def main():
    folder_to_scan = sys.argv[0]
    print(f'start in folder {folder_to_scan}')   
    #scan(Path(folder_to_scan))
    print(f'Images:{IMAGES}')
    print(f'Audio: {MUSIC}')
    print(f'Video: {VIDEO}')
    print(f'Documents:{DOCUMENTS}')
    print(f'Archives: {ARCHIVES}')
    print(f'My_others: {MY_OTHERS}')

    print(FOLDERS[::-1])
    
if __name__ == "__main__":
    main()
    
def start():
    if sys.argv[0]:
        folder_for_scan = Path(sys.argv[0])
        print(f'Start in folder {folder_for_scan.resolve()}')
    
    main(folder_for_scan.resolve())
    
    
