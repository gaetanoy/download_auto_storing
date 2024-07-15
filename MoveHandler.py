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
        create_directories()
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                check_image_files(entry, name)
                check_doc_files(entry, name)
                check_exe_files(entry, name)
                check_zip_files(entry, name)
                check_prog_files(entry, name)
                check_db_files(entry, name)
                check_other_files(entry, name)


def create_dir(directory):
    if not exists(directory):
        os.makedirs(directory)


def create_directories():
    create_dir(dest_dir_img)
    create_dir(dest_dir_doc)
    create_dir(dest_dir_exe)
    create_dir(dest_dir_zip)
    create_dir(dest_dir_prog)
    create_dir(dest_dir_db)
    create_dir(dest_dir_other)


def check_files(entry, name, extensions, dest):
    for extension in extensions:
        if name.endswith(extension) or name.endswith(extension.upper()):
            move_file(dest, entry, name)
            logging.info(f"Moved {name} to {dest}")


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
    move_file(dest_dir_other, entry, name)


def move_file(dest, entry, name):
    if exists(f"{dest}"+r'\\'+f"{name}"):
        unique_name = make_unique(dest, name)
        old_name = join(dest, name)
        new_name = join(dest, unique_name)
        os.rename(old_name, new_name)
    move(entry, dest)


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # si le fichier existe déjà, on itère sur le nom du fichier
    while exists(f"{dest}"+r'\\'+f"{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name









