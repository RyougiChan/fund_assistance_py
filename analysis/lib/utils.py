import os


def get_path(path, current_file=None):
    path = os.path.normpath(path)
    return os.path.join(os.path.dirname(current_file), path) \
        if current_file is not None else os.path.join(os.path.dirname(os.path.dirname(__file__)), path)


def test():
    print(os.path.dirname(__file__))
