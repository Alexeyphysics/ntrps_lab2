"""Модуль собственного класса-итератора для обхода экземпляров класса.

Лабораторная работа №2 по курсу «Новые технологии в РПС».
Выполнил: студент Кондратенко А.С.
Пункт 5: Класс ClassIterator с реализацией методов __iter__ и __next__.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterator, List

import pandas as pd


class ClassIterator(Iterator[str]):
    """Класс-итератор для последовательного обхода файлов заданного класса."""

    def __init__(
        self,
        class_label: str,
        annotation_path: Path | str = "annotation.csv",
    ) -> None:
        """Инициализация итератора.

        :param class_label: Метка требуемого класса (например, '1', '5').
        :param annotation_path: Путь к файлу аннотации.
        """
        self.class_label = str(class_label)
        self.annotation_path = Path(annotation_path)
        self.file_paths: List[str] = self._load_paths()
        self.cursor: int = 0

    def _load_paths(self) -> List[str]:
        """Загружает пути к файлам для своего класса из файла аннотации."""
        if not self.annotation_path.exists():
            print(f"[WARN] Файл {self.annotation_path} не найден.")
            return []

        df = pd.read_csv(self.annotation_path, dtype={"output_class": str})
        filtered_df = df[df["output_class"] == self.class_label]
        return filtered_df["absolute_path"].tolist()

    def __iter__(self) -> ClassIterator:
        """Возвращает сам экземпляр итератора."""
        return self

    def __next__(self) -> str:
        """Возвращает абсолютный путь к следующему файлу класса.

        При исчерпании элементов выбрасывает исключение StopIteration.
        """
        if self.cursor >= len(self.file_paths):
            raise StopIteration

        instance_path = self.file_paths[self.cursor]
        self.cursor += 1
        return instance_path

    def __len__(self) -> int:
        """Возвращает общее количество экземпляров данного класса."""
        return len(self.file_paths)


def parse_arguments() -> argparse.Namespace:
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Итератор по элементам заданного класса датасета."
    )
    parser.add_argument(
        "--class_label",
        type=str,
        default="1",
        help="Метка класса (по умолчанию: 1)",
    )
    parser.add_argument(
        "--annotation",
        type=str,
        default="annotation.csv",
        help="Путь к аннотации (по умолчанию: annotation.csv)",
    )
    return parser.parse_args()


def main() -> None:
    """Демонстрация работы класса-итератора ClassIterator."""
    args = parse_arguments()
    target_class = args.class_label
    print(f"=== Демонстрация ClassIterator для класса '{target_class}' ===")

    review_iterator = ClassIterator(
        class_label=target_class,
        annotation_path=args.annotation,
    )
    print(f"[ИНФО] Найдено элементов для обхода: {len(review_iterator)}")

    # 1. Обход с помощью цикла for (стандартный протокол Python)
    print("\n--- 1. Обход через цикл for ---")
    for idx, path in enumerate(review_iterator, start=1):
        print(f"[{idx:02d}] {path}")

    # 2. Проверка генерации StopIteration при прямом вызове next()
    print("\n--- 2. Проверка исчерпания итератора ---")
    try:
        next(review_iterator)
    except StopIteration:
        print("[УСПЕХ] Итератор штатно выбросил исключение StopIteration!")


if __name__ == "__main__":
    main()
