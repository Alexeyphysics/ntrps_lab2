"""Модуль получения следующего экземпляра заданного класса.

Лабораторная работа №2 по курсу «Новые технологии в РПС».
Выполнил: студент Кондратенко А.С.
Пункт 4: Функция get_next_instance, возвращающая путь к очередному
экземпляру класса без повторений или None при исчерпании.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

# Реестр путей и указателей для каждого класса
_CLASS_DATA: Dict[str, List[str]] = {}
_CLASS_POINTERS: Dict[str, int] = {}


def load_dataset_by_annotation(
    annotation_path: Path | str = "annotation.csv",
) -> Dict[str, List[str]]:
    """Загружает пути к файлам, сгруппированные по меткам классов из CSV.

    :param annotation_path: Путь к файлу-аннотации.
    :return: Словарь вида {метка_класса: [список_абсолютных_путей]}.
    """
    csv_file = Path(annotation_path)
    if not csv_file.exists():
        print(f"[WARN] Файл аннотации {csv_file} не найден.")
        return {}

    df = pd.read_csv(csv_file, dtype={"output_class": str})
    grouped_data: Dict[str, List[str]] = {}

    for class_label, group in df.groupby("output_class"):
        grouped_data[str(class_label)] = group["absolute_path"].tolist()

    return grouped_data


def init_instance_registry(
    annotation_path: Path | str = "annotation.csv",
) -> None:
    """Инициализирует реестр данных и сбрасывает указатели выборки.

    :param annotation_path: Путь к CSV аннотации.
    """
    global _CLASS_DATA, _CLASS_POINTERS
    _CLASS_DATA = load_dataset_by_annotation(annotation_path)
    _CLASS_POINTERS = {cls_name: 0 for cls_name in _CLASS_DATA}


def get_next_instance(
    class_label: str,
    annotation_path: Path | str = "annotation.csv",
) -> Optional[str]:
    """Возвращает путь к следующему неповторяющемуся экземпляру класса.

    Когда все экземпляры класса исчерпаны, возвращает None.

    :param class_label: Метка требуемого класса (например, '1', '5').
    :param annotation_path: Путь к файлу аннотации.
    :return: Абсолютный путь к файлу или None.
    """
    # Ленивая инициализация при первом вызове функции
    if not _CLASS_DATA:
        init_instance_registry(annotation_path)

    cls_key = str(class_label)
    if cls_key not in _CLASS_DATA:
        return None

    current_idx = _CLASS_POINTERS.get(cls_key, 0)
    class_files = _CLASS_DATA[cls_key]

    if current_idx >= len(class_files):
        return None

    next_file_path = class_files[current_idx]
    _CLASS_POINTERS[cls_key] = current_idx + 1
    return next_file_path


def parse_arguments() -> argparse.Namespace:
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Последовательное извлечение экземпляров класса."
    )
    parser.add_argument(
        "--class_label",
        type=str,
        default="1",
        help="Метка класса для теста (по умолчанию: 1)",
    )
    parser.add_argument(
        "--annotation",
        type=str,
        default="annotation.csv",
        help="Путь к аннотации (по умолчанию: annotation.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Демонстрация работы функции get_next_instance."""
    args = parse_arguments()
    target = args.class_label
    print(f"=== Тестирование get_next_instance для класса '{target}' ===")

    step = 1
    while True:
        instance_path = get_next_instance(
            target,
            annotation_path=args.annotation,
        )
        if instance_path is None:
            print(f"[ЗАВЕРШЕНИЕ] Экземпляры класса '{target}' исчерпаны.")
            break
        print(f"Шаг {step:02d}: Путь -> {instance_path}")
        step += 1

    # Повторная попытка возвращает None
    check_none = get_next_instance(
        target,
        annotation_path=args.annotation,
    )
    print(f"[ПРОВЕРКА] Повторный вызов вернул: {check_none}")


if __name__ == "__main__":
    main()
