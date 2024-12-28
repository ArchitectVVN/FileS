import os
import json
import datetime

class FileInfo:
    """
    Класс для хранения информации о файле:
      - filename (имя файла, без пути)
      - full_path (полный путь к файлу)
      - file_size (размер в байтах)
      - creation_date (дата создания в формате ISO-строки)
      - last_modified (дата последнего изменения в формате ISO-строки)
    """
    def __init__(self, filename, full_path, file_size, creation_date, last_modified):
        self.filename = filename
        self.full_path = full_path
        self.file_size = file_size
        self.creation_date = creation_date
        self.last_modified = last_modified

    def to_dict(self):
        """
        Преобразование объекта в словарь (для удобной сериализации в JSON).
        """
        return {
            "filename": self.filename,
            "full_path": self.full_path,
            "file_size": self.file_size,
            "creation_date": self.creation_date,
            "last_modified": self.last_modified
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Восстановление объекта FileInfo из словаря (при десериализации).
        """
        return cls(
            filename=data["filename"],
            full_path=data["full_path"],
            file_size=data["file_size"],
            creation_date=data["creation_date"],
            last_modified=data["last_modified"]
        )

def gather_file_info():
    """
    Сканируем директорию `data/processed/` и собираем информацию о каждом файле в список объектов FileInfo.
    Затем сериализуем эти данные в JSON-файл `file_info.json`.
    """
    project_root = "project_root"
    processed_dir = os.path.join(project_root, "data", "processed")
    output_json = os.path.join(project_root, "output", "file_info.json")
    
    file_info_list = []

    if not os.path.isdir(processed_dir):
        print(f"Директория не найдена: {processed_dir}")
        return

    # Обходим все файлы в папке processed
    for filename in os.listdir(processed_dir):
        full_path = os.path.join(processed_dir, filename)
        if os.path.isfile(full_path):
            stats = os.stat(full_path)
            
            # Даты создания и изменения (в формате ISO: YYYY-MM-DD HH:MM:SS)
            # Обратите внимание, что на Windows ctime = время создания,
            # на Unix-системах ctime — время изменения метаданных.
            creation_date = datetime.datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            last_modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            file_info = FileInfo(
                filename=filename,
                full_path=full_path,
                file_size=stats.st_size,
                creation_date=creation_date,
                last_modified=last_modified
            )
            file_info_list.append(file_info)
    
    # Сериализуем список объектов FileInfo в JSON
    data_to_serialize = [f.to_dict() for f in file_info_list]
    
    # Сохраняем в файл
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as jf:
        json.dump(data_to_serialize, jf, ensure_ascii=False, indent=4)
    
    print(f"Файл с информацией о файлах создан: {output_json}")

def restore_file_info():
    """
    Читаем JSON-файл `file_info.json` и восстанавливаем объекты FileInfo.
    """
    project_root = "project_root"
    input_json = os.path.join(project_root, "output", "file_info.json")
    
    if not os.path.isfile(input_json):
        print(f"JSON-файл не найден: {input_json}")
        return
    
    with open(input_json, "r", encoding="utf-8") as jf:
        data = json.load(jf)
    
    # Восстанавливаем список объектов FileInfo
    file_info_list = [FileInfo.from_dict(item) for item in data]
    
    print("Десериализация прошла успешно. Содержимое объектов FileInfo:")
    for fi in file_info_list:
        print(fi.filename, fi.full_path, fi.file_size, fi.creation_date, fi.last_modified)

def main():
    # Собираем информацию и сериализуем
    gather_file_info()
    # Проверяем, что данные можно десериализовать обратно
    restore_file_info()

if __name__ == "__main__":
    main()
