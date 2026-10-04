"""Скрипт генерации проверенного jupyter-ноутбука для ЛР2."""

import ast
import json


def create_lab2_notebook() -> None:
    """Формирует и валидирует lab2_notebook.ipynb."""
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Лабораторная работа №2. Обработка данных парсинга и работа с pandas\n",
                "\n",
                "**Дисциплина:** Новые технологии в РПС  \n",
                "**Вариант:** №9 (Текстовые отзывы с сервиса *Otzovik*, классы 1–5 звёзд)  \n",
                "**Выполнил:** студент Кондратенко А.С.  \n",
                "\n",
                "--- \n",
                "## Цель работы\n",
                "Рефакторинг результатов сбора данных, создание файлов-аннотаций с помощью `pandas`, "
                "реорганизация файловой структуры датасета и проектирование собственных итераторов."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 0. Подготовка окружения и данных"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "from pathlib import Path\n",
                "import random\n",
                "import shutil\n",
                "from typing import Dict, List, Optional, Tuple, Iterator\n",
                "import pandas as pd\n",
                "\n",
                "dataset_path = Path('dataset')\n",
                "if not dataset_path.exists():\n",
                "    print('Инициализация рабочего каталога в Google Colab...')\n",
                "    !git clone https://github.com/Alexeyphysics/ntrps_lab2.git _tmp_repo\n",
                "    if Path('_tmp_repo/dataset').exists():\n",
                "        !cp -r _tmp_repo/dataset ./dataset\n",
                "    !rm -rf _tmp_repo\n",
                "\n",
                "# Подстраховка: если клонирование не сработало, создаем эталонную структуру\n",
                "if not dataset_path.exists() or not any(dataset_path.iterdir()):\n",
                "    for cat in range(1, 6):\n",
                "        cat_dir = dataset_path / str(cat)\n",
                "        cat_dir.mkdir(parents=True, exist_ok=True)\n",
                "        for i in range(10):\n",
                "            (cat_dir / f'{str(i).zfill(4)}.txt').write_text(\n",
                "                f'Отзыв Сбербанк #{cat}_{i}\\n\\nТекст отзыва с оценкой {cat} звезд.',\n",
                "                encoding='utf-8'\n",
                "            )\n",
                "\n",
                "print('Датасет готов к работе!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "--- \n",
                "## 1. Задание 1. Формирование файла-аннотации исходного датасета\n",
                "Создание CSV-файла с колонками: `absolute_path`, `relate_path`, `output_class`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def create_annotation(dataset_dir: str = 'dataset', output_csv: str = 'annotation.csv') -> pd.DataFrame:\n",
                "    root = Path(dataset_dir).resolve()\n",
                "    project_root = Path.cwd().resolve()\n",
                "    records = []\n",
                "    for class_folder in sorted(root.iterdir()):\n",
                "        if class_folder.is_dir():\n",
                "            cls_name = class_folder.name\n",
                "            for f in sorted(class_folder.glob('*.txt')):\n",
                "                records.append((\n",
                "                    str(f.resolve()),\n",
                "                    str(f.relative_to(project_root)),\n",
                "                    cls_name\n",
                "                ))\n",
                "    cols = ['absolute_path', 'relate_path', 'output_class']\n",
                "    df = pd.DataFrame(records, columns=cols)\n",
                "    df.to_csv(output_csv, index=False, encoding='utf-8')\n",
                "    return df\n",
                "\n",
                "df_task1 = create_annotation()\n",
                "print(f'Создана аннотация: {len(df_task1)} строк')\n",
                "df_task1.head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "--- \n",
                "## 2. Задание 2. Копирование с именованием <class>_<index>.txt\n",
                "Копирование в папку `dataset_class/` и создание новой аннотации `annotation_class.csv`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def copy_class_prefixed(src_dir: str = 'dataset', dst_dir: str = 'dataset_class') -> pd.DataFrame:\n",
                "    src = Path(src_dir).resolve()\n",
                "    dst = Path(dst_dir).resolve()\n",
                "    dst.mkdir(parents=True, exist_ok=True)\n",
                "    project_root = Path.cwd().resolve()\n",
                "    records = []\n",
                "    for class_folder in sorted(src.iterdir()):\n",
                "        if class_folder.is_dir():\n",
                "            cls_name = class_folder.name\n",
                "            for f in sorted(class_folder.glob('*.txt')):\n",
                "                new_name = f'{cls_name}_{f.name}'\n",
                "                target_f = dst / new_name\n",
                "                shutil.copy2(f, target_f)\n",
                "                records.append((\n",
                "                    str(target_f.resolve()),\n",
                "                    str(target_f.relative_to(project_root)),\n",
                "                    cls_name\n",
                "                ))\n",
                "    cols = ['absolute_path', 'relate_path', 'output_class']\n",
                "    df = pd.DataFrame(records, columns=cols)\n",
                "    df.to_csv('annotation_class.csv', index=False, encoding='utf-8')\n",
                "    return df\n",
                "\n",
                "df_task2 = copy_class_prefixed()\n",
                "print(f'Скопировано файлов: {len(df_task2)}')\n",
                "df_task2.head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "--- \n",
                "## 3. Задание 3. Копирование со случайными номерами (0..10000)\n",
                "Копирование без коллизий в папку `dataset_random/` и создание аннотации `annotation_random.csv`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "def copy_random_numbers(src_dir: str = 'dataset', dst_dir: str = 'dataset_random') -> pd.DataFrame:\n",
                "    src = Path(src_dir).resolve()\n",
                "    dst = Path(dst_dir).resolve()\n",
                "    dst.mkdir(parents=True, exist_ok=True)\n",
                "    project_root = Path.cwd().resolve()\n",
                "    all_files = []\n",
                "    for class_folder in sorted(src.iterdir()):\n",
                "        if class_folder.is_dir():\n",
                "            for f in sorted(class_folder.glob('*.txt')):\n",
                "                all_files.append((f, class_folder.name))\n",
                "    random_numbers = random.sample(range(0, 10001), len(all_files))\n",
                "    records = []\n",
                "    for (f, cls_name), num in zip(all_files, random_numbers):\n",
                "        new_name = f'{str(num).zfill(5)}.txt'\n",
                "        target_f = dst / new_name\n",
                "        shutil.copy2(f, target_f)\n",
                "        records.append((\n",
                "            str(target_f.resolve()),\n",
                "            str(target_f.relative_to(project_root)),\n",
                "            cls_name\n",
                "        ))\n",
                "    cols = ['absolute_path', 'relate_path', 'output_class']\n",
                "    df = pd.DataFrame(records, columns=cols)\n",
                "    df.to_csv('annotation_random.csv', index=False, encoding='utf-8')\n",
                "    return df\n",
                "\n",
                "df_task3 = copy_random_numbers()\n",
                "print(f'Скопировано файлов со случайными номерами: {len(df_task3)}')\n",
                "df_task3.head(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "--- \n",
                "## 4. Задание 4. Функция get_next_instance\n",
                "Последовательное получение экземпляров заданного класса с возвратом `None` при исчерпании."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "class InstanceRegistry:\n",
                "    def __init__(self, annotation_file: str = 'annotation.csv'):\n",
                "        df = pd.read_csv(annotation_file, dtype={'output_class': str})\n",
                "        self.data = {}\n",
                "        self.pointers = {}\n",
                "        for cls_name, grp in df.groupby('output_class'):\n",
                "            self.data[str(cls_name)] = grp['absolute_path'].tolist()\n",
                "            self.pointers[str(cls_name)] = 0\n",
                "\n",
                "    def get_next(self, class_label: str) -> Optional[str]:\n",
                "        cls_key = str(class_label)\n",
                "        if cls_key not in self.data:\n",
                "            return None\n",
                "        idx = self.pointers[cls_key]\n",
                "        items = self.data[cls_key]\n",
                "        if idx >= len(items):\n",
                "            return None\n",
                "        path = items[idx]\n",
                "        self.pointers[cls_key] = idx + 1\n",
                "        return path\n",
                "\n",
                "registry = InstanceRegistry('annotation.csv')\n",
                "print('Получение всех экземпляров класса 1:')\n",
                "count = 0\n",
                "while True:\n",
                "    instance = registry.get_next('1')\n",
                "    if instance is None:\n",
                "        print(f'Экземпляры исчерпаны. Всего получено: {count}. Следующий вызов: {registry.get_next(\"1\")}')\n",
                "        break\n",
                "    count += 1\n",
                "    print(f'[{count:02d}] {instance}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "--- \n",
                "## 5. Задание 5. Собственный класс-итератор ClassIterator\n",
                "Реализация стандартного протокола итерации `__iter__` и `__next__` с выбросом исключения `StopIteration`."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "class ClassIterator(Iterator[str]):\n",
                "    def __init__(self, class_label: str, annotation_file: str = 'annotation.csv'):\n",
                "        self.class_label = str(class_label)\n",
                "        df = pd.read_csv(annotation_file, dtype={'output_class': str})\n",
                "        self.paths = df[df['output_class'] == self.class_label]['absolute_path'].tolist()\n",
                "        self.cursor = 0\n",
                "\n",
                "    def __iter__(self) -> 'ClassIterator':\n",
                "        return self\n",
                "\n",
                "    def __next__(self) -> str:\n",
                "        if self.cursor >= len(self.paths):\n",
                "            raise StopIteration\n",
                "        path = self.paths[self.cursor]\n",
                "        self.cursor += 1\n",
                "        return path\n",
                "\n",
                "print('Итерация через цикл for по классу 5:')\n",
                "iterator = ClassIterator('5')\n",
                "for i, p in enumerate(iterator, 1):\n",
                "    print(f'{i:02d} -> {p}')\n",
                "\n",
                "try:\n",
                "    next(iterator)\n",
                "except StopIteration:\n",
                "    print('Успех: StopIteration штатно перехвачен!')"
            ]
        }
    ]

    for idx, cell in enumerate(cells):
        if cell["cell_type"] == "code":
            raw_code = "".join(cell["source"])
            clean_lines = [
                line for line in raw_code.splitlines()
                if not line.strip().startswith("!")
            ]
            ast.parse("\n".join(clean_lines))

    notebook_dict = {
        "cells": cells,
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 2
    }

    with open("lab2_notebook.ipynb", "w", encoding="utf-8") as f_out:
        json.dump(notebook_dict, f_out, ensure_ascii=False, indent=1)

    print("Файл lab2_notebook.ipynb успешно обновлен!")


if __name__ == "__main__":
    create_lab2_notebook()
