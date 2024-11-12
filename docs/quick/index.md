# О проекте

В настоящее время FastTower находится в ранней стадии разработки. Буквально с момента создания первого файла и до релиза v0.1.6
прошло 4 дня с перерывом на 2 месяца. Вследствие этого имеются проблемы например с зависимостями для запуска проекта, когда не
используется tortoise и aerich - их все равно потребуется установить, а cli всегда будет говорить о не установленной
FASTTOWER_SETTINGS_MODULE переменной(Даже на этапе создания проекта - он напомнит об этом xdd).

Но не будем о плохом. Проект работает и будет улучшаться!

## Установка

=== "pip"
    ```bash
    pip install fasttower[tortoise]
    pip install git+https://github.com/pysashapy/taerich.git@0.0.1
    ```

=== "poetry"
    ```bash
    poetry add fasttower[tortoise] git+https://github.com/pysashapy/taerich.git@0.0.1
    ```