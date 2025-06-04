# Lagrange Method Solver

Приложение для решения задач методом множників Лагранжа з графічним інтерфейсом.

## Вимоги

- Python 3.8 або вище
- pip (менеджер пакетів Python)

## Встановлення

1. Клонуйте репозиторій:
```bash
git clone https://github.com/your-username/lagrange.git
cd lagrange
```

2. Створіть віртуальне середовище:
```bash
# Для Windows
python -m venv venv
venv\Scripts\activate

# Для macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

## Запуск

1. Переконайтеся, що віртуальне середовище активоване:
```bash
# Для Windows
venv\Scripts\activate

# Для macOS/Linux
source venv/bin/activate
```

2. Запустіть програму:
```bash
python main.py
```

## Використання

1. Введіть кількість змінних та обмежень
2. Введіть цільову функцію та обмеження
3. Слідуйте інструкціям на кожному етапі для пошуку екстремуму функції

## Структура проекту

- `main.py` - головний файл програми
- `lagrange_step*.py` 