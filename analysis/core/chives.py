import re

from analysis.lib.utils import ran_str, md5_digest
from analysis.models import Chives


def add_chives(login_name: str, login_password: str):
    if login_name is None or login_password is None:
        return
    pattern_login_name = re.compile(r'\w{4,16}')
    pattern_login_password = re.compile(r'\w{8,32}')
    if pattern_login_name.match(login_name) is False or pattern_login_password.match(login_password) is False:
        return
    if Chives.objects.filter(login_name=login_name).count() > 0:
        return
    salt = ran_str(32)
    encrypt_password = md5_digest(login_password + salt)
    chives = {
        'login_name': login_name,
        'login_password': encrypt_password,
        'salt': salt,
        'nickname': login_name
    }
    a = Chives.objects.create(**chives)
    return a

