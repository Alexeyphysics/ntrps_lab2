"""Модуль копирования датасета с объединением метки класса и имени файла.

Лабораторная работа №2 по курсу «Новые технологии в РПС».
Выполнил: студент Кондратенко А.С.
Пункт 2: Копирование в единую папку вида dataset_class/class_0000.txt
и генерация соответствующего CSV файла-аннотации.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
from typing import List, Tuple

import pandas as pd


def copy_and_rename_dataset(
    src_dir: Path | str,
    dst_dir: Path | str,
) -> List[Tuple[str, str, str]]:
    """Копирует файлы датасета в плоскую директорию с новым форматом имени.

    Формат нового имени: <class>_<original_name>.txt (например, 1_0000.txt).

    :param src_dir: Исходный каталог с подпапками классов.
    :param dst_dir: Целевой каталог для скопированных файлов.
    :return: Список кортежей метаданных для формирования аннотации.
    """
    source_path = Path(src_dir).resolve()
    target_path = Path(dst_dir).resolve()
    project_root = Path.cwd().resolve()
    records: List[Tuple[str, str, str]] = []

    target_path.mkdir(parents=True, exist_ok=True)

    for class_folder in sorted(source_path.iterdir()):
        if not class_folder.is_dir():
            continue

        class_name = class_folder.name
        for src_file in sorted(class_folder.glob("*.txt")):
            # Формируем имя файла вида: 1_0000.txt
            new_file_name = f"{class_name}_{src_file.name}"
            dst_file = target_path / new_file_name

            # Безопасное копирование файла
            shutil.copy2(src_file, dst_file)

            abs_path = str(dst_file.resolve())
            rel_path = str(dst_file.relative_to(project_root))
            records.append((abs_path, rel_path, class_name))

    return records


def save_annotation_csv(
    records: List[Tuple[str, str, str]],
    output_csv: Path | str,
) -> None:
    """Создает и сохраняет файл-аннотацию для нового расположения датасета.

    :param records: Список метаданных файлов.
    :param output_csv: Путь к сохраняемому CSV-файлу.
    """
    columns = ["absolute_path", "relate_path", "output_class"]
    df = pd.DataFrame(data=records, columns=columns)
    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"[ИНФО] Файл-аннотация сохранен: {out_path.resolve()}")


def parse_arguments() -> argparse.Namespace:
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Копирование датасета с именованием <class>_<index>.txt."
    )
    parser.add_argument(
        "--src",
        type=str,
        default="dataset",
        help="Исходный каталог датасета (по умолчанию: dataset)",
    )
    parser.add_argument(
        "--dst",
        type=str,
        default="dataset_class",
        help="Целевой каталог (по умолчанию: dataset_class)",
    )
    parser.add_argument(
        "--annotation",
        type=str,
        default="annotation_class.csv",
        help="Имя CSV-файла аннотации (по умолчанию: annotation_class.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Точка входа скрипта второго задания."""
    args = parse_arguments()
    print("=== Старт копирования датасета с модификацией имен ===")
    records = copy_and_rename_dataset(args.src, args.dst)
    print(f"[ИНФО] Успешно скопировано файлов: {len(records)}")

    save_annotation_csv(records, args.annotation)
    print("=== Задание 2 успешно завершено! ===")


if __name__ == "__main__":
    main()
