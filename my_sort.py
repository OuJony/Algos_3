"""Быстрая сортировка списков и консольная утилита для сортировки файлов."""

import argparse
from functools import cmp_to_key
from pathlib import Path
from random import randint, randrange
from typing import Any, Callable, Iterator, List, Optional, Tuple, TypeVar, Union


Item = TypeVar("Item")
Entry = Tuple[Any, Item]


def _quick_sort_steps(entries: List[Entry], reverse: bool) -> Iterator[None]:
    """Разбивает список на части и делает паузу после каждого разбиения."""
    bounds = [(0, len(entries))]
    while bounds:
        start, stop = bounds.pop()
        if stop - start < 2:
            continue

        pivot = entries[randrange(start, stop)][0]
        smaller, equal, greater = [], [], []
        for entry in entries[start:stop]:
            value = entry[0]
            if value < pivot:
                smaller.append(entry)
            elif pivot < value:
                greater.append(entry)
            else:
                equal.append(entry)

        first, last = (greater, smaller) if reverse else (smaller, greater)
        entries[start:stop] = first + equal + last
        yield None

        bounds.append((stop - len(last), stop))
        bounds.append((start, start + len(first)))


def my_sort(
    array: List[Item],
    reverse: bool = False,
    key: Optional[Callable[[Item], Any]] = None,
    cmp: Optional[Callable[[Any, Any], int]] = None,
) -> List[Item]:
    """Возвращает новый список, сохраняя порядок элементов с равными ключами.
    key вычисляется один раз для каждого элемента.
    """
    wrap = cmp_to_key(cmp) if cmp is not None else None
    entries = []
    for item in array:
        value = key(item) if key is not None else item
        entries.append((wrap(value) if wrap is not None else value, item))

    for _ in _quick_sort_steps(entries, reverse):
        pass

    return [item for _, item in entries]


def _positive_size(value: str) -> int:
    """Проверяет размер списка для демонстрации."""
    size = int(value)
    if size < 1:
        raise argparse.ArgumentTypeError("Размер списка должен быть больше нуля.")
    return size


def _show_steps(size: int, reverse: bool) -> None:
    """Показывает разбиения случайного списка в консоли."""
    values = [randint(-99, 99) for _ in range(size)]
    entries = [(value, value) for value in values]
    _show_frame("Исходный список", entries)
    for step, _ in enumerate(_quick_sort_steps(entries, reverse), start=1):
        _show_frame(f"Шаг {step}", entries)
    _show_frame("Результат", entries)


def _show_frame(label: str, entries: List[Tuple[int, int]]) -> None:
    """Печатает числа и столбики, высота которых соответствует их значениям."""
    values = [value for _, value in entries]
    heights = "▁▂▃▄▅▆▇█"
    # Высоты от 0 до 7 соответствуют диапазону от -99 до 99.
    bars = " ".join(heights[(value + 99) * 7 // 198] for value in values)
    print(f"{label}: {values}\n{bars}")


def main() -> None:
    """Разбирает аргументы и запускает сортировку файла или демонстрацию."""
    parser = argparse.ArgumentParser(description="Быстрая сортировка")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="Входной файл, по одному элементу на строку")
    source.add_argument("--visualize", type=_positive_size, help="Размер случайного списка")
    parser.add_argument("--output", type=Path, help="Файл для результата")
    parser.add_argument("--type", choices=("number", "text"), default="number",
                        help="Тип данных в файле (по умолчанию number)")
    parser.add_argument("--reverse", action="store_true", help="Сортировать по убыванию")
    args = parser.parse_args()

    if args.visualize is not None:
        if args.output is not None:
            parser.error("--output используется для сортировки файла")
        _show_steps(args.visualize, args.reverse)
        return

    try:
        lines = args.input.read_text(encoding="utf-8-sig").splitlines()
        if args.type == "number":
            # Пустые строки пропускает. Целые числа сравнивает без округления.
            numbers = [line.strip() for line in lines if line.strip()]
            result = my_sort(numbers, reverse=args.reverse, key=_parse_number)
        else:
            result = my_sort(lines, reverse=args.reverse)
        output = "".join(f"{item}\n" for item in result)
        if args.output is None:
            print(output, end="")
        else:
            args.output.write_text(output, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.error(str(error))


def _parse_number(value: str) -> Union[int, float]:
    """Читает целое или вещественное число из строки."""
    try:
        return int(value)
    except ValueError:
        return float(value)


if __name__ == "__main__":
    main()
