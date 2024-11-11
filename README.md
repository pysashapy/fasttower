<p align="center">
  <a href="https://pysashapy.github.io/fasttower/"><img src="docs/img/logo.png" alt="FastTower"  width="256"></a>
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

[Документация](https://pysashapy.github.io/fasttower/)

## Features

- Легкая настройка
- Высокая производительность
- Простота в использовании
- Админ панель

## Быстрый старт

В настоящее время официально поддерживаться только tortoise orm и админ панель для нее, но вы можете легко добавить свою
поддержку бд модернизируя
FastTower app в asgi.py файле

[Полный пример](https://github.com/pysashapy/fasttower/tree/main/examples/maximun_example)

### Установка

```console
pip install fasttower[tortoise]
```

Так же для управления миграциями требуется aerich, а именно его модернизированный форк

```console
pip install git+https://github.com/pysashapy/taerich.git@0.0.1
```

### Создание проекта

Для начала требуется сгенерировать основное приложение

```console
tower g p example
```

После выполнения команды, вы можете обнаружить Django-like структуру проекта и сразу же запустить сервер!

```console
python manage.py run
```

<details markdown="1">
<summary>Или другим сервером...</summary>

```
uvicorn example.asgi:app 
```

</details>

### Commands

Список текущих команд и их описания вы можете получить используя команду

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
│ run         Запуск FastTower сервера                                                                                                                                                                                           │
│ shell       Запускает интерактивную оболочку.                                                                                                                                                                                  │
│ superuser   Create a superuser.                                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
