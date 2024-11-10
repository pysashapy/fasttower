# FastTower

FastTower — это мощная и легкая библиотека для быстрого создания серверных приложений на Python с Django-like структурой.

## Features

- Легкая настройка
- Высокая производительность
- Простота в использовании

## Быстрый старт
В настоящее время поддерживаться только tortoise orm, но вы можете легко добавить свою поддержку бд модернизируя FastTower app в asgi.py.
### Установка
```bash
pip install fasttower[tortoise]
```
Так же для управления миграция требуется aerich, а именно его модернизированный форк.
```bash
pip install git+https://github.com/pysashapy/taerich.git@0.0.1
```
### Создание проекта 
Для начала требуется сгенерировать основное приложение
```bash
tower g p example
```
После выполнения команды, вы можете обнаружить Django-like структуру проекта и сразу же запустить сервер
```bash
python manage.py run
```
<details markdown="1">
<summary>Или другим сервером...</summary>
```bash
uvicorn example.asgi:app 
```
</details>
### Обзор
Главная роль manage.py файла установить env **FASTTOWER_SETTINGS_MODULE** указывающею путь до вашего settings. Вы можете установить ее сами и после этого использовать команду **tower**
<details markdown="1">
<summary>Запуск с установленной env...</summary>
```bash
tower run
```
</details>

