import os
import glob


def list_all_dir_files_with_folder(folder):
    return glob.glob(folder + "*")


def list_all_dir_files(folder):
    return os.listdir(folder)
