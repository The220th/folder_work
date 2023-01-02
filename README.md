# folder_work

Скрипты, которые позволяют работать с директориями

# Зависимости

``` bash
> pip3 install --upgrade pip

> pip3 install tabulate # Опциональные
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
> python folder_work.py diff {n|c|r|i} {folder_old} {folder_new} #, где:
#   n (new): Покажет новые файлы
#   c (changed): Покажет изменённые файлы
#   r (removed): Покажет удалённые файлы
#   i (identical): Покажет идентичные файлы
#   Или любая их комбинация
```
