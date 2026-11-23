# Как запускать программу:

1) По возрастанию, от меньшего к большему (из файла): python my_sort.py --input input.txt
2) По убыванию, от большего к меньшему (из файла): python my_sort.py --input input.txt --reverse
3) С сохранением результата в output.txt: python my_sort.py --input input.txt --output output.txt
4) Сортировка текста. Нужно записать в words.txt по одному слову или фразе на строку и запустить: python -X utf8 my_sort.py --input words.txt --type text
5) Пошаговая визуализация. Программа сама сгенерирует 10 случайных чисел и покажет, как они сортируются. Для убывания добавь --reverse: python -X utf8 my_sort.py --visualize 10

# Тесты

1) python -m unittest -v
2) py -3.13 -m pylint --rcfile=.pylintrc my_sort.py

