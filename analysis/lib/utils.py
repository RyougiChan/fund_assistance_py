import os
import hashlib
import random
import string


def get_path(path, current_file=None):
    path = os.path.normpath(path)
    return os.path.join(os.path.dirname(current_file), path) \
        if current_file is not None else os.path.join(os.path.dirname(os.path.dirname(__file__)), path)


def absolute_file_paths(directory):
    paths = []
    for dir_path, _, filenames in os.walk(directory):
        for f in filenames:
            paths.append(os.path.abspath(os.path.join(dir_path, f)))
    return paths


def ran_str(length: int):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def md5_digest(s: str):
    if s is not None:
        m = hashlib.md5()
        m.update(s.encode("utf8"))
        return m.hexdigest()
    return None


def test():
    a = absolute_file_paths(get_path('data/raw'))
    print(a)
    print(ran_str(32))
