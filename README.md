# KazakhBench 🇰🇿

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/kazakhbench)
![GitHub issues](https://img.shields.io/github/issues/yourusername/kazakhbench)
![GitHub stars](https://img.shields.io/github/stars/yourusername/kazakhbench)
![GitHub forks](https://img.shields.io/github/forks/yourusername/kazakhbench)
![GitHub license](https://img.shields.io/github/license/yourusername/kazakhbench)

```
     ____  __    ___    ___    __  __ __  ____     ___  ____   ____   __  __ __ 
    |    \|  |  /  _]  /  _]  /  ]|  |  ||    \   /  _]|    \ |    \ |  ||  |  |
    |  o  )  | /  [_  /  [_  /  / |  |  ||  _  | /  [_ |  o  )|  o  )|  ||  |  |
    |   _/|  ||    _]|    _]/  /  |  _  ||  |  ||    _]|     ||     ||__||  |  |
    |  |  |  ||   [_ |   [_/   \_ |  |  ||  |  ||   [_ |  O  ||  O  ||  ||  :  |
    |  |  |  ||     ||     \     ||  |  ||  |  ||     ||     ||     ||  ||     |
    |__| |__||_____||_____|\____||__|__||__|__||_____||_____||_____||__| \__,_|
```

[🇰🇿 Қазақша](./README_KK.md) | [🇬🇧 English](./README.md) | [🇷🇺 Русский](./README_RU.md)

</div>

Тілдік модельдердің қазақ тілін білу деңгейін бағалауға арналған кешенді бенчмарк. KazakhBench тілдік модельдердің қазақ тілімен жұмыс істеу қабілетін бағалауға арналған стандартталған тест жиынтығын ұсынады.

## 📋 Мазмұны

- [Ерекшеліктері](#ерекшеліктері)
- [Жұмысты бастау](#жұмысты-бастау)
- [Құрылымы](#құрылымы)
- [Қолдану](#қолдану)
- [Жобаға үлес қосу](#жобаға-үлес-қосу)
- [Лицензия](#лицензия)

## ✨ Ерекшеліктері

- **5 бағалау категориясы:**
  - 🗣 Тілдік түсіну (30%)
  - 🧠 Логикалық ойлау (25%)
  - 🔢 Математикалық қабілеттер (25%)
  - 🏺 Мәдени білім (10%)
  - 📚 Контекстік түсіну (10%)

- **4 тестілеу форматы:**
  - Көп таңдаулы сұрақтар (MCQ)
  - Еркін жауап сұрақтары (FRQ)
  - Толықтыру тапсырмалары (CT)
  - Пайымдау тапсырмалары (RT)

## 🚀 Жұмысты бастау

```bash
# Репозиторийді клондау
git clone https://github.com/yourusername/kazakhbench.git

# Тәуелділіктерді орнату
cd kazakhbench
pip install -r requirements.txt

# Тестілеуді бастау
python evaluate.py --model your_model_name
```

## 📁 Құрылымы

```
kazakhbench/
├── benchmarks/           # Тест жинақтары
│   ├── linguistic/       # Тілдік түсіну
│   ├── logical/         # Логикалық ойлау
│   ├── mathematical/    # Математикалық қабілеттер
│   ├── cultural/        # Мәдени білім
│   └── contextual/      # Контекстік түсіну
├── src/                 # Бастапқы код
│   ├── evaluation/      # Бағалау скриптері
│   └── utils/          # Көмекші функциялар
└── examples/           # Қолдану мысалдары
```

## 📊 Бағалау әдістемесі

### Метрикалар

| Категория | Салмағы | Метрикалар |
|-----------|---------|------------|
| Тілдік түсіну | 30% | Accuracy, BLEU, ROUGE |
| Логикалық ойлау | 25% | Accuracy, Custom metrics |
| Математикалық қабілеттер | 25% | Accuracy, Step-by-step evaluation |
| Мәдени білім | 10% | Accuracy, Expert evaluation |
| Контекстік түсіну | 10% | BLEU, ROUGE, Expert evaluation |

### Бағалау мысалы

```python
from kazakhbench import evaluate_model

results = evaluate_model(
    model="your_model",
    tasks=["linguistic", "logical", "mathematical"],
    weights={"linguistic": 0.3, "logical": 0.25, "mathematical": 0.25}
)
```

## 🤝 Жобаға үлес қосу

Жобаның дамуына үлес қосуға қош келдіңіз! Сіз:

1. 🐛 Қателер туралы хабарлай аласыз
2. ✨ Жаңа функциялар ұсына аласыз
3. 📝 Құжаттаманы жақсарта аласыз
4. 🔧 Pull request жібере аласыз

[Үлес қосу нұсқаулығымен](CONTRIBUTING.md) танысып шығыңыз.

## 📚 Тест мысалдары

### Тілдік түсіну

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
    "explanation": "Қатаң 'п' дыбысынан кейін 'тың' жалғауы жалғанады"
}
```

### Логикалық ойлау

```json
{
    "task_id": "log_001",
    "type": "RT",
    "question": "Барлық сәбилер еңбектейді. Айша - сәби. Қорытынды жасаңыз.",
    "reference_answer": "Айша еңбектейді",
    "reasoning_steps": [
        "Сәбилер туралы жалпы пайымдау",
        "Нақты жағдай (Айша)",
        "Логикалық қорытынды"
    ]
}
```

## 📄 Лицензия

Бұл жоба MIT License бойынша лицензияланған - толық ақпарат алу үшін [LICENSE](LICENSE) файлын қараңыз.

## 📞 Байланыс

- LinkedIn: [KazakhBench](https://linkedin.com/in/kazakhbench)
- Telegram: [@kazakhbench](https://t.me/kazakhbench)

---

<div align="center">
Қазақ NLP қауымдастығы үшін ❤️ жасалған
</div>
