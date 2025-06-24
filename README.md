<!--Start-->

#### 💻 Фреймворк автоматизации тестирования мобильного приложения "Google Keep" 

#### Цель проекта:

- Сценарий проверки функциональности.
  - Создание, удаление заметок.
  - Тестирование UI/UX.
  - Поддержка разных устройств через конфигурации.
  - Генерация отчетов с помощью Allure для анализа результатов тестирования.

#### Технологический стеk:

| Компонент            | Версия      | Назначение                          |
|----------------------|-------------|-------------------------------------|
| [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png" width="20"> **Python**](https://www.python.org/) | `3.13.3` | Основной язык |
| [<img src="https://docs.pytest.org/en/7.4.x/_static/pytest_logo_curves.svg" width="53">](https://docs.pytest.org/) | `7.4.0` | Тест-фреймворк |
[![Appium](https://img.shields.io/badge/-Appium-FF2D20?logo=appium&logoColor=white&style=flat&logoWidth=20&cacheSeconds=3600)](https://appium.io/) | `2.19.0` | Мобильная автоматизация |
| [<img src="https://avatars.githubusercontent.com/u/3221291?s=200&v=4" width="20"> **Appium-inspector**](https://github.com/appium/appium) | `3.1` | Инспектор элементов (для разработки и отладки, не обязателен для запуска) |
| [<img src="https://developer.android.com/studio/images/studio-icon.svg" width="20"> **Android Studio**](https://developer.android.com/studio) | `Merkat 3.1` | Эмулятор Android |
| [<img src="https://code.visualstudio.com/assets/images/code-stable.png" width="20"> **VS Code**](https://code.visualstudio.com/) | `1.65.2` | IDE разработки |
| [<img src="https://avatars.githubusercontent.com/u/5879127?s=200&v=4" width="20"> **Allure**](https://docs.qameta.io/allure/) | `2.34.0` | Отчётность |

#### Структура проекта: 

```bash
📁 mobile_automation_framework/
├── 📄 README.md                    # Основная документация проекта
├── 📂 allure-results/              # Отчеты Allure
├── ⚙️ config/                      # Конфигурация управление настройками
│   └── 📂 capabilities/            # Настройки устройств
│       └── 📱Pixel_2_API_27.json   # Профиль устройства
├── 💻 core/                        # Ядро фреймворка
│   ├── 📄 base_page.py             # Базовый Page Object
│   └── 📄 driver.py                # Appium драйвер
├── 📑 pages/                       # Page Objects
│   ├── 📄 main_page.py             # Главная страница
│   ├── 📄 note_page.py             # Работа с заметками
│   └── 📄 labels_page.py           # Управление метками
├── 📦 requirements/                # Зависимости
│   ├── 📄 base.txt                 # Основные пакеты
│   └── 📄 dev.txt                  # Инструменты разработки
├── 📸 screenshots/                 # Скриншоты ошибок
├── 🧪 tests/                       # Тестовые сценарии
│   ├── 📄 conftest.py              # Фикстуры pytest
│   └── 📂 smoke/                   # Smoke-тесты
│       ├── 📄 test_check_ui_ux.py  # Проверки UI
│       ├── 📄 test_create_note.py  # Создание заметок
│       └── 📄 test_delete_note.py  # Удаление заметок
└  🛠️ utils/                        # Вспомогательные модули
    ├── 📄 logger.py                # Логирование
    └── 📄 screenshot.py            # Создание скриншотов
```

#### 🚀 Запуск проекта: 
##### Установить зависимости:

1. [Python 3](https://www.python.org/downloads/macos/) 
 ```bash
# Проверь установку:
python3 --version
```

2. [Appium](https://github.com/appium/appium) 
 ```bash
# Установка Appium:
npm install -g appium
# Проверь установленную версию Appium:
appium --version
# Запустить Appium Server в отдельном терминале:
appium 
```

3. [Android Studio + SDK](https://developer.android.com/studio?hl=ru) 
 ```bash
# Создать эмулятор и убедиться что он доступен 
emulator -list-avds
# Запустить эмулятор 
emulator -avd Pixel_2 -netdelay none -netspeed full
```

4. Перейди в папку проекта:
 ```bash
# Перейди в папку проекта:
cd ~/Desktop/mobile_automation_framework
```

5. Запустить тесты:
 ```bash
# Запуск всех тестов по маске
pytest tests -v
# Запуска одного конкретного теста 
pytest tests/smoke/test_create_note.py -v
# Запуск всех тестов с отчетом 
pytest tests --alluredir=./allure-results
# Открытие отчёта:
allure serve ./allure-results
```
<!--End-->
