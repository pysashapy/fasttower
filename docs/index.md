<p align="center">
  <a href="https://pysashapy.github.io/fasttower/"><img src="img/logo.png" alt="FastTower"  width="256"></a>
</p>
<p align="center">
    <em>FastTower — это молодой фреймворк основанный на FastAPI для быстрого создания серверных приложений с Django-like структурой.</em>
</p>
<p align="center">
<a href="https://pypi.org/project/fasttower" target="_blank">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fasttower">
</a>
<a href="https://pypi.org/project/fasttower" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fasttower.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

## Features

- Легкая настройка
- Высокая производительность
- Простота в использовании
- Админ панель

## Быстрый старт

### Установка
В настоящее время официально поддерживаться только tortoise orm и админ панель для нее, но вы можете легко добавить свою
поддержку бд модернизируя FastTower app в asgi.py файле

=== "pip"
    ```bash
    pip install fasttower[tortoise]
    pip install git+https://github.com/pysashapy/taerich.git@0.0.1
    ```

=== "poetry"
    ```bash
    poetry add fasttower[tortoise] git+https://github.com/pysashapy/taerich.git@0.0.1
    ```

!!! danger "Временная проблема"
    В настоящее время обязательно требуется установка именно **fasttower[tortoise]** и **taerich.git**, в будущих релизах мы избавим вас от этих обязательных зависимостей!


### Создание проекта

Для начала создайте проект командой:

```console
tower g p example
```
После выполнения команды, вы можете обнаружить Django-like структуру проекта и сразу же запустить сервер
Он будет доступен по адресу <http://127.0.0.1:8000/docs>

=== "fasttower manage.py"

    ```bash
    python manage.py run
    ```
=== "fasttower tower"

    ```bash
    tower run
    ```
    !!! note
        Перед испольвазнием **tower** для запуска сервера, работы с бд и т.д. Убедитесь что установлена переменная окружения FASTTOWER_SETTINGS_MODULE

=== "uvicorn"

    ```bash
    uvicorn example.asgi:app 
    ```

=== "hypercorn"

    ```bash
    hypercorn example.asgi:app 
    ```

!!! example "Полный пример"

    Пример содержит отправку писем по SMTP, кэширование, добавление новых команд, tortoise-orm, lifespans 
    [Github](https://github.com/pysashapy/fasttower/tree/main/examples/maximun_example)

### Команды

Список доступных команд и их описания вы можете получить используя

```console
tower --help
```

```text
 Usage: tower [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                         

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                        │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                 │
│ --help                        Show this message and exit.                                                                                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ db          Database commands                                                                                                                                                                                                  │
│ g           Generate project structures and app components for FastTower.                                                                                                                                                      │
│ run         Start the FastTower server                                                                                                                                                                                         │
│ shell       Launch an interactive shell.                                                                                                                                                                                       │
│ superuser   Create a superuser.                                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
