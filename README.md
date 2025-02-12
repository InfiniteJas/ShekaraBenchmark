# ShekaraBenchmark

# KazakhBench 🇰🇿

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/kazakhbench)
![GitHub issues](https://img.shields.io/github/issues/yourusername/kazakhbench)
![GitHub stars](https://img.shields.io/github/stars/yourusername/kazakhbench)
![GitHub forks](https://img.shields.io/github/forks/yourusername/kazakhbench)
![GitHub license](https://img.shields.io/github/license/yourusername/kazakhbench)

[🇰🇿 Қазақша](./README_KK.md) | [🇬🇧 English](./README.md)

</div>

Комплексный бенчмарк для оценки казахскоязычных языковых моделей. KazakhBench предоставляет стандартизированный набор тестов для оценки способностей языковых моделей в работе с казахским языком.

## 📋 Содержание

- [Особенности](#особенности)
- [Начало работы](#начало-работы)
- [Структура](#структура)
- [Использование](#использование)
- [Вклад в проект](#вклад-в-проект)
- [Лицензия](#лицензия)

## ✨ Особенности

- **5 категорий оценки:**
  - 🗣 Языковое понимание (30%)
  - 🧠 Логическое мышление (25%)
  - 🔢 Математические способности (25%)
  - 🏺 Культурные знания (10%)
  - 📚 Контекстное понимание (10%)

- **4 формата тестирования:**
  - Multiple Choice Questions (MCQ)
  - Free Response Questions (FRQ)
  - Completion Tasks (CT)
  - Reasoning Tasks (RT)

## 🚀 Начало работы

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/kazakhbench.git

# Установка зависимостей
cd kazakhbench
pip install -r requirements.txt

# Запуск тестов
python evaluate.py --model your_model_name
```

## 📁 Структура

```
kazakhbench/
├── benchmarks/           # Тестовые наборы
│   ├── linguistic/       # Языковое понимание
│   ├── logical/         # Логическое мышление
│   ├── mathematical/    # Математические способности
│   ├── cultural/        # Культурные знания
│   └── contextual/      # Контекстное понимание
├── src/                 # Исходный код
│   ├── evaluation/      # Скрипты оценки
│   └── utils/          # Вспомогательные функции
└── examples/           # Примеры использования
```

## 📊 Методология оценки

### Метрики

| Категория | Вес | Метрики |
|-----------|-----|---------|
| Языковое понимание | 30% | Accuracy, BLEU, ROUGE |
| Логическое мышление | 25% | Accuracy, Custom metrics |
| Математические способности | 25% | Accuracy, Step-by-step evaluation |
| Культурные знания | 10% | Accuracy, Expert evaluation |
| Контекстное понимание | 10% | BLEU, ROUGE, Expert evaluation |

### Пример оценки

```python
from kazakhbench import evaluate_model

results = evaluate_model(
    model="your_model",
    tasks=["linguistic", "logical", "mathematical"],
    weights={"linguistic": 0.3, "logical": 0.25, "mathematical": 0.25}
)
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Вы можете:

1. 🐛 Сообщать об ошибках
2. ✨ Предлагать новые функции
3. 📝 Улучшать документацию
4. 🔧 Отправлять pull request'ы

Пожалуйста, ознакомьтесь с нашим [руководством по внесению вклада](CONTRIBUTING.md).

## 📚 Примеры тестов

### Языковое понимание

```json
{
    "task_id": "morph_001",
    "type": "MCQ",
    "question": "Берілген сөздің дұрыс жалғауын таңдаңыз: Кітап___ үстелде жатыр",
    "options": [
        "A) тың",
        "B) тің",
        "C) дың",
        "D) дің"
    ],
    "correct": "A",
    "explanation": "После глухого согласа 'п' используется жалғау 'тың'"
}
```

### Логическое мышление

```json
{
    "task_id": "log_001",
    "type": "RT",
    "question": "Барлық сәбилер еңбектейді. Айша - сәби. Қорытынды жасаңыз.",
    "reference_answer": "Айша еңбектейді",
    "reasoning_steps": [
        "Универсальное утверждение о сәби",
        "Конкретный случай (Айша)",
        "Логический вывод"
    ]
}
```

## 📈 Результаты

| Модель | Общий счет | Языковое понимание | Логика | Математика | Культура | Контекст |
|--------|------------|-------------------|---------|------------|-----------|-----------|
| GPT-4 | 85.3 | 87.2 | 84.5 | 86.1 | 82.4 | 83.8 |
| СНС-3 | 82.1 | 84.3 | 81.7 | 83.2 | 80.1 | 81.5 |

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Контакты

- Website: [kazakhbench.kz](https://kazakhbench.kz)
- Email: contact@kazakhbench.kz
- Twitter: [@kazakhbench](https://twitter.com/kazakhbench)

---

<div align="center">
Made with ❤️ for Kazakh NLP Community
</div>

