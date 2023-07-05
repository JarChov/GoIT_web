import shutil
import re
import sys
from pathlib import Path
from threading import Thread

folders = []
unknown_extensions = set()
known_extensions = set()

files_manager = {
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'odt', 'xls'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'archives': ['zip', 'gz', 'tar', '7z'],
    'scripts': ['py'],
    'unknown_extension': []
    }

sorted_elements = {
    'images': [],
    'video': [],
    'documents': [],
    'audio': [],
    'archives': [],
    'scripts': [],
    'unknown_extension': []
}


def folders_finder(path: Path):
    '''пошук всіх файлів та папок в заданому шляху'''

    for element in path.iterdir():
        if element.is_dir():
            if element.name not in files_manager.keys():
                folders.append(element)
                folders_finder(element)
        else:
            th = Thread(target=file_mover, args=(element, path,))
            th.start()
            # file_mover(element, path)


def file_mover(file: Path, output_dir: Path) -> None:
    is_file_copy = False
    file_extension = file.suffix[1:]
    file_extension_normalized = file.suffix
    file_name = normalize(file.name.removesuffix(file_extension_normalized)) + file_extension_normalized

    for key, value in files_manager.items():
        for extension in value: # пошук розширення в значеннях словника
            if file_extension.lower() == extension:
                known_extensions.add(file_extension)
                new_dir = output_dir / key / extension
                new_dir.mkdir(exist_ok=True, parents=True)
                if file_extension in files_manager['archives']:
                    archive_name = normalize(str(file.name.removesuffix('.zip' or '.tar' or '.gz')))
                    archive_dir = output_dir / key / archive_name
                    archive_dir.mkdir(exist_ok=True, parents=True)
                    archive_extractor(file, archive_dir)
                    is_file_copy = True
                else:
                    file.replace(new_dir / file_name)
                    is_file_copy = True

                # запис скопійованих файлів у відповідні списки
                if key in sorted_elements.keys():
                    sorted_elements[key].append(file.name)

    if not is_file_copy: # якщо невідоме розширення, то:
        unknown_extensions.add(file_extension)
        new_dir = output_dir / 'unknown_extension'
        new_dir.mkdir(exist_ok=True)
        file.replace(new_dir / file_name)
        sorted_elements['unknown_extension'].append(file.name)


def copied_files() -> None:
    for category, file_items in sorted_elements.items():
        if file_items:
            print(f'sorted files to category {category}: ')
            print('*' * 30)
            for file in file_items:
                print(file)


def archive_extractor(file: Path, path: Path):
    try:
        shutil.unpack_archive(file, path)
    except shutil.ReadError:
        print(f'Cannot unpack archive {file.name}')
    else:
        file.unlink()

    return


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(file_name: str) -> str:
    normalized_name = file_name.translate(TRANS)
    normalized_name = re.sub(r'\W', '_', normalized_name)
    return normalized_name


def delete_folder() -> None:
    for folder in folders:
        try:
            folder.rmdir()
        except OSError:
            print(f"Can't delete the folder: {folder}")


def main() -> None:
    path = Path(sys.argv[1])
    folders_finder(path)

    copied_files()
    delete_folder()
    if known_extensions:
        print(f'sorted known_extensions is: {known_extensions}')
    if unknown_extensions:
        print(f'sorted unknown_extensions is: {unknown_extensions}')


if __name__ == '__main__':
    main()
