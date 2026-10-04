# Лабораторная работа №2. Обработка данных парсинга и работа с pandas

**Дисциплина:** Новые технологии в РПС  
**Вариант:** №9 (Текстовые отзывы с сервиса *Otzovik*, классы оценок 1–5 звёзд)  
**Выполнил:** студент Кондратенко А.С.

---

## 📁 Структура проекта
Каждое задание вынесено в отдельный модуль в соответствии с регламентом:
- `task1.py` — формирование CSV-аннотации исходного датасета (`annotation.csv`).
- `task2.py` — копирование в `dataset_class/` с именами `<class>_<index>.txt` и аннотацией `annotation_class.csv`.
- `task3.py` — копирование в `dataset_random/` со случайными номерами (0..10000) без коллизий и аннотацией `annotation_random.csv`.
- `task4.py` — функция `get_next_instance(class_label)` с возвратом `None` при исчерпании элементов.
- `task5.py` — собственный класс-итератор `ClassIterator` с поддержкой `__iter__` и `__next__`.
- `lab2_notebook.ipynb` — интерактивный jupyter-ноутбук (Google Colab).
- `build_notebook.py` — генератор валидированного блокнота.

---

## 🚀 Запуск модулей
```bash
# Активация окружения
source venv/bin/activate

# Запуск каждого пункта:
python3 task1.py
python3 task2.py
python3 task3.py
python3 task4.py --class_label 1
python3 task5.py --class_label 5

# Проверка соответствия стандарту PEP8:
flake8 task1.py task2.py task3.py task4.py task5.py
