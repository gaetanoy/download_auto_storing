import logging
import os
from os.path import exists, splitext, join
from watchdog.events import FileSystemEventHandler
from shutil import move
from type import (image_extensions, doc_extensions, exe_extensions, zip_extensions,prog_extensions, db_extensions)
from dir import (source_dir, dest_dir_img, dest_dir_doc, dest_dir_exe, dest_dir_zip, dest_dir_prog, dest_dir_db,
                 dest_dir_other)


class MoveHandler(FileSystemEventHandler):

    def on_modified(self, event):
        """
        - Crée les répertoires de destination (si besoin)
        - Parcourt les fichiers dans le répertoire source.
        - Traite et déplace les fichiers selon leur type en évitant les doublons et les fichiers temporaires.
        """
        create_directories()
        # set to keep track of processed files to avoid attempt of moving the same file multiple times
        processed_files = []

        with os.scandir(source_dir) as entries:
            for entry in entries:
                # skip directories and temporary files
                if not entry.is_file() or entry.name.endswith('.tmp'):
                    continue
                name = entry.name
                # skip files that have already been processed
                if name in processed_files:
                    continue
                processed_files.append(name)

                check_image_files(entry, name)
                check_doc_files(entry, name)
                check_exe_files(entry, name)
                check_zip_files(entry, name)
                check_prog_files(entry, name)
                check_db_files(entry, name)
                check_other_files(entry, name)


def create_dir(directory):
    """
    Crée un répertoire s'il n'existe pas.
    :param directory: chemin du répertoire
    :return:
    """
    if not exists(directory):
        os.makedirs(directory)


def create_directories():
    """
    Crée tous les répertoires de destination nécessaires
    :return:
    """
    create_dir(dest_dir_img)
    create_dir(dest_dir_doc)
    create_dir(dest_dir_exe)
    create_dir(dest_dir_zip)
    create_dir(dest_dir_prog)
    create_dir(dest_dir_db)
    create_dir(dest_dir_other)


def check_files(entry, name, extensions, dest):
    """
    Vérifie si le fichier est du type attendu et le déplace dans le répertoire de destination.
    :param entry: fichier à déplacer
    :param name: nom du fichier
    :param extensions: liste des extensions de fichiers attendues
    :param dest: répertoire de destination
    :return:
    """
    for extension in extensions:
        if name.endswith(extension) or name.endswith(extension.upper()):
            move_file(dest, entry, name)
            logging.info(f"Moved {name} to {dest}")
            break


def check_image_files(entry, name):
    check_files(entry, name, image_extensions, dest_dir_img)


def check_doc_files(entry, name):
    check_files(entry, name, doc_extensions, dest_dir_doc)


def check_exe_files(entry, name):
    check_files(entry, name, exe_extensions, dest_dir_exe)


def check_zip_files(entry, name):
    check_files(entry, name, zip_extensions, dest_dir_zip)


def check_prog_files(entry, name):
    check_files(entry, name, prog_extensions, dest_dir_prog)


def check_db_files(entry, name):
    check_files(entry, name, db_extensions, dest_dir_db)


def check_other_files(entry, name):
    if os.path.exists(entry):
        move_file(dest_dir_other, entry, name)


def move_file(dest, entry, name):
    """
    Déplace un fichier vers le répertoire de destination.
    Gère les erreurs potentielles comme les permissions, les fichiers non trouvés ou d'autres exceptions.
    Renomme les fichiers pour éviter les conflits.
    :param dest: Chemin du répertoire de destination
    :param entry: fichier à déplacer
    :param name: nom du fichier
    :return:
    """
    destination_path = join(dest, name)
    if exists(destination_path):
        unique_name = make_unique(dest, name)
        new_name = join(dest, unique_name)
        os.rename(destination_path, new_name)
    try:
        move(entry, dest)
    except PermissionError as e:
        logging.warning(f"Failed to move {name} to {dest}. Reason: {e}.")
    except FileNotFoundError as e:
        logging.error(f"Failed to find {name} at {entry.path}. It may have been moved or deleted. Error: {e}")
    except Exception as e:
        logging.error(f"Failed to move {name} due to an unexpected error: {e}")


def make_unique(dest, name):
    """
    Génère un nom de fichier unique en cas de conflit dans le répertoire de destination.
    :param dest: Chemin du répertoire de destination
    :param name: Fichier à déplacer
    :return:
    """
    filename, extension = splitext(name)
    counter = 1
    # si le fichier existe déjà, on itère sur le nom du fichier
    while exists(f"{dest}"+r'\\'+f"{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name









