import os
import json
import chardet
import datetime

# Путь к корневой папке проекта
PROJECT_ROOT = "project_root"

# Поддиректории
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

###############################################################################
# Вспомогательная функция для определения кодировки файла
###############################################################################
def detect_encoding(file_path, sample_size=4096):
    """
    Определяем кодировку файла, читая первый кусок размером sample_size байт.
    По умолчанию: 4096 байт. Можно увеличить, если файлы крупные.
    """
    with open(file_path, "rb") as f:
        raw_data = f.read(sample_size)
    result = chardet.detect(raw_data)
    encoding = result["encoding"]
    # Если chardet не смог уверенно определить, подставим 'utf-8' по умолчанию
    if not encoding:
        encoding = "utf-8"
    return encoding

###############################################################################
# Вспомогательная функция для преобразования: upper -> lower, lower -> upper
###############################################################################
def swap_case(text):
    """
    Меняем регистр:
    - заглавные буквы -> строчные
    - строчные -> заглавные
    """
    return "".join(char.lower() if char.isupper() else char.upper() for char in text)

###############################################################################
# 1. Чтение файлов из data/raw/, преобразование и сохранение в data/processed/
###############################################################################
def process_files():
    """
    1) Считывает все файлы из data/raw/.
    2) Определяет кодировку и читает исходный текст.
    3) Преобразует содержимое.
    4) Сохраняет с суффиксом _processed в data/processed/.
    Возвращает список словарей:
       [ { 'filename': ..., 'original_text': ..., 'processed_text': ... }, ... ]
    """
    processed_info = []

    # Получаем список файлов в raw
    files_in_raw = os.listdir(RAW_DIR)
    for filename in files_in_raw:
        raw_path = os.path.join(RAW_DIR, filename)
        
        # Пропускаем, если вдруг попадутся не-файлы (директории)
        if not os.path.isfile(raw_path):
            continue
        
        # Определяем кодировку
        encoding = detect_encoding(raw_path)
        
        # Считываем содержимое
        with open(raw_path, "r", encoding=encoding, errors="replace") as f:
            original_text = f.read()
        
        # Преобразуем
        processed_text = swap_case(original_text)
        
        # Формируем имя выходного файла
        base, ext = os.path.splitext(filename)
        processed_filename = f"{base}_processed{ext}"
        processed_path = os.path.join(PROCESSED_DIR, processed_filename)
        
        # Сохраняем обработанное содержимое
        # Сохраняем в UTF-8 (или в ту же кодировку, если нужно).
        with open(processed_path, "w", encoding="utf-8") as f:
            f.write(processed_text)

        # Сохраняем в список, чтобы потом сериализовать в JSON
        processed_info.append({
            "filename": processed_filename,
            "original_text": original_text,
            "processed_text": processed_text
        })
    
    return processed_info

###############################################################################
# 2. Сериализация данных в один JSON-файл processed_data.json
###############################################################################
def serialize_processed_data():
    """
    1) Для всех файлов из data/processed/ собираем сведения:
        - Имя файла
        - Исходный текст (уже получаем из предварительной функции process_files, если нужно)
        - Преобразованный текст
        - Размер файла (байты)
        - Дата последнего изменения (строка в удобном формате)
    2) Записываем итоговый список в output/processed_data.json
    """
    # Для удобства: повторно вызываем process_files(), чтобы:
    #   - обеспечить чтение новых файлов
    #   - или можно сохранить результаты process_files() в переменную
    # В данном примере: допустим, что уже вызвали process_files()
    
    # Собираем актуальный список файлов из папки processed
    processed_files = os.listdir(PROCESSED_DIR)
    data_for_json = []
    
    for filename in processed_files:
        processed_path = os.path.join(PROCESSED_DIR, filename)
        if not os.path.isfile(processed_path):
            continue
        
        # Считываем текущее содержимое (уже "processed")
        with open(processed_path, "r", encoding="utf-8", errors="replace") as f:
            processed_content = f.read()
        
        # Информация о файле
        file_stat = os.stat(processed_path)
        file_size = file_stat.st_size
        modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
        
        # Вытаскиваем исходный текст (нам нужен "original_text").
        # Но мы уже потеряли "original_text" при записи файла, ведь записан только processed_text.
        # Поэтому "original_text" берём из сохранённой структуры process_files() (см. ниже).
        
        data_for_json.append({
            "filename": filename,
            "processed_text": processed_content,
            "file_size_bytes": file_size,
            "last_modified": modification_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Запишем всё в JSON
    output_file_path = os.path.join(OUTPUT_DIR, "processed_data.json")
    with open(output_file_path, "w", encoding="utf-8") as json_f:
        json.dump(data_for_json, json_f, ensure_ascii=False, indent=4)

    print(f"JSON-файл успешно записан: {output_file_path}")


###############################################################################
# Объединяем логику:
###############################################################################
def main():
    """
    1. Обработка сырых файлов (raw) -> сохранение обработанных (processed).
    2. Сериализация в один JSON-файл в output/.
    
    Чтобы отобразить в JSON ещё и 'original_text', 
    стоит сохранять результаты process_files() и использовать их.
    """
    # 1) Обрабатываем файлы, получаем список словарей
    processed_records = process_files()
    
    # 2) Преобразуем (дополняем) эти записи информацией о размере/датах и пишем в JSON
    # Сейчас serialize_processed_data() считывает processed-файлы "с нуля".
    # Если нужно в итоге *также* включить original_text в JSON, 
    # давайте совместим подходы:
    
    # (a) Собираем данные о размерe и дате модификации
    results_for_json = []
    for record in processed_records:
        # record = {"filename": ..., "original_text": ..., "processed_text": ...}
        processed_path = os.path.join(PROCESSED_DIR, record["filename"])
        if os.path.isfile(processed_path):
            file_stat = os.stat(processed_path)
            file_size = file_stat.st_size
            modification_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)
            # Добавляем поля
            record["file_size_bytes"] = file_size
            record["last_modified"] = modification_time.strftime("%Y-%m-%d %H:%M:%S")
        
        results_for_json.append(record)

    # (b) Записываем всё в JSON
    output_file_path = os.path.join(OUTPUT_DIR, "processed_data.json")
    with open(output_file_path, "w", encoding="utf-8") as json_f:
        json.dump(results_for_json, json_f, ensure_ascii=False, indent=4)

    print(f"JSON-файл успешно записан: {output_file_path}")


if __name__ == "__main__":
    main()
