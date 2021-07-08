import os


def get_path(path, current_file=None):
    return os.path.join(os.path.dirname(current_file), path) if current_file is not None else os.path.join(os.path.dirname(__file__), path)
