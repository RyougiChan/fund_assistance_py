# 配置注意事项

## 系统信息

Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-144-generic x86_64)

## python 版本选择

### 内置版本

```sh
python --version
>> Python 2.7.17
python3 --version
>> Python 3.6.9
```

Ubuntu 内置版本 Python 2.7.17
Ubuntu 内置版本 Python 3.6.9

### 另外安装的版本

Python 3.8.11
> 为什么：很多开发环境使用的 Python 版本都比较高，有些特性是在新版本才引入的，如使用 Python 3.6 版本运行 `datetime.fromisoformat()` 时会报错 `type object 'datetime.datetime' has no attribute 'fromisoformat'`，原因是这个方法是 Python 3.7 才引入的。

#### 安装方法

##### 使用 Apt

01. 以 root 或具有 sudo 访问权限的用户身份运行以下命令以更新软件包列表并安装先决条件：

    ```sh
    sudo apt update
    sudo apt install software-properties-common
    ```

02. 将 deadsnakes PPA 添加到系统的源列表中：

    ```sh
    sudo add-apt-repository ppa:deadsnakes/ppa
    ```

    出现提示时按 Enter 继续：

    ```sh
    OUTPUT:
    Press [ENTER] to continue or Ctrl-c to cancel adding it.
    ```

03. 启用存储库后，使用以下命令安装 Python 3.8：

    ```sh
    sudo apt install python3.8
    ```

04. 验证安装是否成功：

    ```sh
    python3.8 --version
    >> Python 3.8.11
    ```

##### 从源码安装

01. 更新包列表并安装构建 Python 所需的包：

    ```sh
    sudo apt update
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
    ```

02. 使用 wget 从 Python 下载页面下载最新版本的源代码：

    ```sh
    wget https://www.python.org/ftp/python/3.8.11/Python-3.8.11.tgz
    ```

03. 下载完成后，解压 gzip 压缩包：

    ```sh
    tar -xf Python-3.8.11.tgz
    ```

04. 切换到 Python 源目录并执行配置脚本，该脚本执行多项检查以确保系统上的所有依赖项都存在：

    ```sh
    cd Python-3.8.11
    ./configure --enable-optimizations
    ```

    `--enable-optimizations` 选项通过运行多个测试来优化 Python 二进制文件。这会使构建过程变慢。

05. 启动 Python 3.8 构建过程：

    ```sh
    make -j 8
    ```

    为了加速构建过程，请修改 `-j` 以对应处理器中的内核数。您可以通过键入 `nproc` 找到该数字。

06. 构建过程完成后，键入以下命令安装 Python 二进制文件：

    ```sh
    sudo make altinstall
    ```

    ❌不要使用标准的 make install ，因为它会覆盖默认的系统 python3 二进制文件。

07. 验证安装是否成功：

    ```sh
    python3.8 --version
    >> Python 3.8.11
    ```

#### pip 设置

01. 默认的 pip3 命令会将依赖包安装到内置的 3.6 版本的仓库，因此可选择重新指定一个命令

    ```sh
    alias pip3='python3.8 -m pip'
    ```

02. 升级 pip

    ```sh
    pip3.8 install --upgrade pip
    ```

## 如何重置 Python

误操作后的重置方法

```sh
sudo update-alternatives --config python
>> update-alternatives: error: no alternatives for python

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
>> update-alternatives: using /usr/bin/python3.6 to provide /usr/bin/python (python) in auto mode

sudo update-alternatives --config python
>> There is only one alternative in link group python (providing /usr/bin/python): /usr/bin/python3.6
>> Nothing to configure.

sudo update-alternatives  --set python /usr/bin/python3.6
python --version
>> Python 3.6.9
```

## 参考

[【Djangoの本番環境構築】Ubuntu20.04,Python3.8,Nginx,Gunicorn,PostgreSQL](https://tomato-develop.com/django-ubuntu-python-nginx-gunicorn-postgresql/)
