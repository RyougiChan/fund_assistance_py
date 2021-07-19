# Fund simulation trade

![fund simulation](analysis/data/logo.png)

Some indicators are always used to predict stock's trends, for example, [MACD Oscillator](https://en.wikipedia.org/wiki/MACD), [Bollinger Bands Pattern](https://en.wikipedia.org/wiki/Bollinger_Bands), [Hikkake Pattern](https://en.wikipedia.org/wiki/Hikkake_pattern), and etc. The project aim to make simulation trade with **fund** using some scientific technical indicators(we use [Bollinger Bands Pattern](https://en.wikipedia.org/wiki/Bollinger_Bands) in the project now).

## Requirements

Before you can start, the following dependencies need to be installed.

- Python with version>=3.7
- pip
- The following python dependencies

```sh
pip install django akshare plotly kaleido PyJWT PyYAML aliyun-python-sdk-sts aliyun-python-sdk-core oss2 alibabacloud_sts20150401 timeloop
```

## Usage

```sh
cd <root of project>
python manage.py runserver
```

For server deployment, following this guide save my life: [【Djangoの本番環境構築】Ubuntu20.04,Python3.8,Nginx,Gunicorn,PostgreSQL](https://tomato-develop.com/django-ubuntu-python-nginx-gunicorn-postgresql/)

## Error recording

```sh
# Python Error
(<class 'AttributeError'>, AttributeError("'HttpResponse' object has no attribute 'headers'"), <traceback object at 0x7f46aeacae80>)
```

```sh
# Solution
pip3 install --upgrade Django
```

---

```sh
# Error
django.core.exceptions.ImproperlyConfigured: SQLite 3.9.0 or later is required (found 3.7.17).
```

```sh
# Solution
# Download source code
wget https://www.sqlite.org/2019/sqlite-autoconf-3360000.tar.gz
# Compile
tar zxvf sqlite-autoconf-3360000.tar.gz 
cd sqlite-autoconf-3360000/
./configure --prefix=/usr/local
make && make install
 
# Replace system low version sqlite3
mv /usr/bin/sqlite3  /usr/bin/sqlite3_old
ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3
echo "/usr/local/lib" > /etc/ld.so.conf.d/sqlite3.conf
ldconfig
sqlite3 -version
```

> Reference: [Upgrade to sqlite3 under centos 7](https://www.programmersought.com/article/93974592356/)

## Declaration

This project is for study and research purposes only and does not constitute any investment advice.

Released under the [Apache License 2.0](LICENSE)
Copyright © [RyougiChan](https://github.com/RyougiChan). All rights reserved.
