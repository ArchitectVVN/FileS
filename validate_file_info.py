import json
import os
from jsonschema import validate, ValidationError, SchemaError

def validate_json_file():
    """
    Валидирует файл file_info.json по схеме file_info_schema.json.
    Выводит результаты валидации или ошибки.
    """
    project_root = "project_root"
    json_path = os.path.join(project_root, "output", "file_info.json")
    schema_path = os.path.join(project_root, "output", "file_info_schema.json")
    
    # 1. Считываем JSON-файл с данными
    if not os.path.isfile(json_path):
        print(f"Не найден JSON-файл с данными: {json_path}")
        return
    
    with open(json_path, "r", encoding="utf-8") as jf:
        data = json.load(jf)
    
    # 2. Считываем JSON Schema
    if not os.path.isfile(schema_path):
        print(f"Не найдена схема: {schema_path}")
        return
    
    with open(schema_path, "r", encoding="utf-8") as sf:
        schema = json.load(sf)
    
    # 3. Проверяем валидность
    try:
        validate(instance=data, schema=schema)
        print("JSON-файл полностью соответствует схеме!")
    except ValidationError as ve:
        print("Обнаружена ошибка в данных JSON-файла:", ve.message)
        print("Путь к ошибке:", list(ve.path))
    except SchemaError as se:
        print("Ошибка в самой JSON-схеме:", se)

if __name__ == "__main__":
    validate_json_file()
