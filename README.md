# folder_work

Скрипты, которые позволяют работать с директориями.

# Зависимости

``` bash
> pip3 install --upgrade pip

> pip3 install tabulate # Опциональные
```

# Установка

Скачайте файл, перенесите его в одну из директорий из `$PATH` и сделайте исполняемым. Например, так:

``` bash
> wget -O ~/.local/bin/folder_work https://raw.githubusercontent.com/The220th/folder_work/main/folder_work.py && chmod u+x ~/.local/bin/folder_work
```

# Хэш директории

``` bash
> python folder_work.py hash {folder_path}
```

# Клонирование директории

``` bash
> python folder_work.py clone {folder_src} {folder_dest}
```

# Поиск повторных (одинаковых) файлов

``` bash
> python folder_work.py repeats {folder_path}
```

# Сравнение двух директорий

``` bash
> python folder_work.py diff {n|c|r|m|i} {folder_old} {folder_new} #, где:
#   n (new): Покажет новые файлы
#   c (changed): Покажет изменённые файлы
#   r (removed): Покажет удалённые файлы
#   m (moved): Покажет переименованные файлы
#   i (identical): Покажет идентичные файлы
#   Или любая их комбинация
```
