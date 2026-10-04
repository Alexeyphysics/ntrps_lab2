"""Модуль копирования датасета со случайной нумерацией файлов.

Лабораторная работа №2 по курсу «Новые технологии в РПС».
Выполнил: студент Кондратенко А.С.
Пункт 3: Копирование в единую папку вида dataset_random/номер.txt
со случайными номерами от 0 до 10000 без коллизий и создание аннотации.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import random
import shutil
from typing import List, Tuple

import pandas as pd


def generate_unique_random_numbers(
    count: int,
    min_val: int = 0,
    max_val: int = 10000,
) -> List[int]:
    """Генерирует заданное количество уникальных случайных чисел.

    Использование random.sample гарантирует отсутствие коллизий и перезаписи.

    :param count: Требуемое количество чисел.
    :param min_val: Минимальное значение диапазона.
    :param max_val: Максимальное значение диапазона.
    :return: Список уникальных случайных чисел.
    """
    total_range = max_val - min_val + 1
    if count > total_range:
        raise ValueError(
            f"Невозможно выбрать {count} чисел " f"из диапазона {total_range}"
        )
    return random.sample(range(min_val, max_val + 1), count)


def copy_dataset_random_names(
    src_dir: Path | str,
    dst_dir: Path | str,
) -> List[Tuple[str, str, str]]:
    """Копирует файлы датасета в целевой каталог со случайными именами.

    Формат нового имени: <random_number:05d>.txt (от 0 до 10000).

    :param src_dir: Исходный каталог датасета.
    :param dst_dir: Целевой каталог для случайных файлов.
    :return: Список кортежей метаданных для создания аннотации.
    """
    source_path = Path(src_dir).resolve()
    target_path = Path(dst_dir).resolve()
    project_root = Path.cwd().resolve()
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. Собираем все исходные файлы и их классы
    file_records: List[Tuple[Path, str]] = []
    for class_folder in sorted(source_path.iterdir()):
        if class_folder.is_dir():
            class_name = class_folder.name
            for src_file in sorted(class_folder.glob("*.txt")):
                file_records.append((src_file, class_name))

    total_files = len(file_records)
    if total_files == 0:
        print("[WARN] Файлы для копирования не найдены.")
        return []

    # 2. Генерируем ровно total_files уникальных случайных номеров
    random_numbers = generate_unique_random_numbers(total_files)

    # 3. Копируем каждый файл с присвоением уникального случайного имени
    annotation_records: List[Tuple[str, str, str]] = []
    for (src_file, class_name), rand_num in zip(file_records, random_numbers):
        new_file_name = f"{str(rand_num).zfill(5)}.txt"
        dst_file = target_path / new_file_name

        shutil.copy2(src_file, dst_file)

        abs_path = str(dst_file.resolve())
        rel_path = str(dst_file.relative_to(project_root))
        annotation_records.append((abs_path, rel_path, class_name))

    return annotation_records


def save_annotation_csv(
    records: List[Tuple[str, str, str]],
    output_csv: Path | str,
) -> None:
    """Сохраняет аннотацию для датасета со случайными именами.

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
        description="Копирование датасета со случайными номерами (0-10000)."
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
        default="dataset_random",
        help="Целевой каталог (по умолчанию: dataset_random)",
    )
    parser.add_argument(
        "--annotation",
        type=str,
        default="annotation_random.csv",
        help="Имя файла аннотации (по умолчанию: annotation_random.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Точка входа скрипта третьего задания."""
    args = parse_arguments()
    print("=== Старт копирования со случайными именами (0..10000) ===")
    records = copy_dataset_random_names(args.src, args.dst)
    print(f"[ИНФО] Скопировано уникальных файлов: {len(records)}")

    save_annotation_csv(records, args.annotation)
    print("=== Задание 3 успешно завершено! ===")


if __name__ == "__main__":
    main()
