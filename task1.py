"""Модуль создания файла-аннотации для исходного датасета.

Лабораторная работа №2 по курсу «Новые технологии в РПС».
Выполнил: студент Кондратенко А.С.
Пункт 1: Формирование CSV файла-аннотации с путями и метками классов.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple

import pandas as pd


def collect_file_annotations(
    dataset_dir: Path | str,
) -> List[Tuple[str, str, str]]:
    """Сканирует каталог датасета и собирает метаданные каждого файла.

    :param dataset_dir: Путь к корневой папке датасета.
    :return: Список кортежей вида (absolute_path, relate_path, output_class).
    """
    root_path = Path(dataset_dir).resolve()
    project_root = Path.cwd().resolve()
    records: List[Tuple[str, str, str]] = []

    if not root_path.exists():
        print(f"[WARN] Каталог {root_path} не найден.")
        return records

    # Проходим по подпапкам классов (например, 1, 2, 3, 4, 5)
    for class_folder in sorted(root_path.iterdir()):
        if class_folder.is_dir():
            class_name = class_folder.name
            for file_path in sorted(class_folder.glob("*.txt")):
                abs_path = str(file_path.resolve())
                # Относительный путь относительно корня текущего проекта
                rel_path = str(file_path.relative_to(project_root))
                records.append((abs_path, rel_path, class_name))

    return records


def build_annotation_dataframe(
    records: List[Tuple[str, str, str]],
) -> pd.DataFrame:
    """Формирует DataFrame pandas на основе списка записей.

    :param records: Список метаданных файлов.
    :return: DataFrame с колонками absolute_path, relate_path, output_class.
    """
    columns = ["absolute_path", "relate_path", "output_class"]
    return pd.DataFrame(data=records, columns=columns)


def save_annotation_csv(df: pd.DataFrame, output_file: Path | str) -> None:
    """Сохраняет DataFrame в CSV файл без числового индекса строк.

    :param df: Исходный DataFrame для сохранения.
    :param output_file: Путь к сохраняемому CSV файлу.
    """
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"[ИНФО] Файл-аннотация успешно сохранен в: {out_path.resolve()}")


def parse_arguments() -> argparse.Namespace:
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Формирование файла-аннотации датасета в формате CSV."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="dataset",
        help="Путь к исходному каталогу датасета (по умолчанию: dataset)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="annotation.csv",
        help="Имя выходного CSV-файла (по умолчанию: annotation.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Основная функция сценария формирования аннотации."""
    args = parse_arguments()
    print("=== Старт создания файла-аннотации ===")
    records = collect_file_annotations(args.dataset)
    print(f"[ИНФО] Найдено файлов для аннотации: {len(records)}")

    df = build_annotation_dataframe(records)
    save_annotation_csv(df, args.output)

    print("\n[РЕЗУЛЬТАТ] Первые 5 строк датафрейма:")
    print(df.head())


if __name__ == "__main__":
    main()
