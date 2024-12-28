import json
import os
from datetime import datetime

def generate_final_report():
    """
    Генерирует итоговый отчёт о выполнении заданий в формате JSON.
    Отчёт включает:
      - Трудности и их решения
      - Время, затраченное на каждый шаг
      - Общие выводы и предложенные улучшения
    Сохраняет отчёт в папку output/ с именем final_report.json
    """
    project_root = "project_root"
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    report_path = os.path.join(output_dir, "final_report.json")
    
    # Пример структуры, которую вы можете заполнить своими реальными данными
    # (время, трудности, выводы и т.д.)
    report_data = {
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tasks": [
            {
                "task_name": "Создание структуры директорий и файлов",
                "difficulties": [
                    "Не сразу разобрался с os.makedirs(exist_ok=True)",
                    "Проблемы с правами доступа на некоторых системах"
                ],
                "solutions": [
                    "Использовал exist_ok=True, чтобы избежать ошибок при повторном запуске",
                    "Работал под пользователем с нужными правами / проверил пути"
                ],
                "time_spent_minutes": 15,
                "conclusions": "Теперь структура создаётся автоматически без ошибок"
            },
            {
                "task_name": "Обработка файлов и сериализация в JSON",
                "difficulties": [
                    "Определение кодировок файлов (chardet)",
                    "Переименование файлов с суффиксом '_processed'"
                ],
                "solutions": [
                    "Установил и использовал библиотеку chardet",
                    "Разделил имя файла через os.path.splitext()"
                ],
                "time_spent_minutes": 20,
                "conclusions": "Файлы корректно обрабатываются, регистры меняются, структура JSON понятна"
            },
            {
                "task_name": "Валидация JSON по схеме (jsonschema)",
                "difficulties": [
                    "Установка правильной версии jsonschema, конфликты зависимостей",
                    "Изначально schema не соответствовала формату данных (проблема с required)"
                ],
                "solutions": [
                    "Установил jsonschema через pip install jsonschema",
                    "Сопоставил поля данных и описание в схеме, поправил required"
                ],
                "time_spent_minutes": 10,
                "conclusions": "JSON теперь валидируется корректно, ошибки выводятся понятно"
            },
            {
                "task_name": "Создание и восстановление резервных копий (backup/restore)",
                "difficulties": [
                    "Проблемы с путями при записи в zip-архив",
                    "Определение правильного пути при restore (на Windows vs Linux)"
                ],
                "solutions": [
                    "Использовал os.path.relpath() для сохранения относительных путей",
                    "Проверил извлечение на разных ОС"
                ],
                "time_spent_minutes": 15,
                "conclusions": "Архивы успешно создаются и восстанавливаются. Папка backups/ работает"
            },
        ],
        
        # Общие выводы и предложения
        "overall_conclusions": "Все задачи выполнены, структура кода ясна, файлы корректно обрабатываются. Проект готов к расширению.",
        "suggested_improvements": [
            "Добавить систему логирования (logging) для детализированного контроля",
            "Реализовать подсчёт реального времени выполнения каждого шага (time.time() или datetime)",
            "Дополнить тестами (pytest) для каждого модуля"
        ]
    }
    
    # Запись в JSON-файл
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=4)
    
    print(f"Итоговый отчёт сгенерирован и сохранён по пути: {report_path}")

def main():
    generate_final_report()

if __name__ == "__main__":
    main()
