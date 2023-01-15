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

# Сравнение изменений в двух директориях

``` bash
> python folder_work.py diff {n|c|r|m|i} {folder_old} {folder_new} #, где:
#   n (new): Покажет новые файлы
#   c (changed): Покажет изменённые файлы
#   r (removed): Покажет удалённые файлы
#   m (moved): Покажет переименованные файлы
#   i (identical): Покажет идентичные файлы
#   Или любая их комбинация
```

# Сравнение двух директорий

``` bash
> python folder_work.py difx {folder1} {folder2}
```

# Выполнение пользовательской команды со всеми файлами

## Выполнение команды для файлов с изменением

``` bash
> python folder_work.py exec {folder_in} {folder_out} {command} #, где
    # {command} - это команда для оболочки, в которой будут заменены:
        # {in} на каждый файл из {folder_in}
        # {out} на каждый файл из {folder_out}
```

Например, сжать все видео файлы в папке `/home/user/in` так, чтобы выходные файлы были в директории `/home/user/out`:

``` bash
> python folder_work.py exec "/home/user/in" "/home/user/out" "ffmpeg -i \"{in}\" -map 0 -vf \"scale=1280:720\" -b:v 1M \"{out}\""
```

## Выполнение команды для файлов без переноса

``` bash
> python folder_work.py exec {folder_in} "" {command} #, где
    # {command} - это команда для оболочки, в которой будут заменены:
        # {in} на каждый файл из {folder_in}
```

Например, проверить тип каждого файла:

``` bash
> python folder_work.py exec "/path/to/files" "" "file \"{in}\" >> output.txt"
```
