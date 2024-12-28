import os
import zipfile

def restore_backup(backup_file_name=None):
    """
    Распаковывает архив (backup_<YYYYMMDD>.zip) из папки backups/
    обратно в data/, восстанавливая структуру директорий и файлы.
    
    Параметр backup_file_name:
      - По умолчанию None: берётся самый новый бэкап из backups/.
      - Или можно указать имя конкретного архива, например "backup_20241228.zip".
    """
    project_root = "project_root"
    data_dir = os.path.join(project_root, "data")
    backups_dir = os.path.join(project_root, "backups")
    
    # Если имя архива не указано, поищем самый новый:
    if backup_file_name is None:
        # Фильтруем только zip-файлы c префиксом "backup_"
        backup_files = [f for f in os.listdir(backups_dir) 
                        if f.startswith("backup_") and f.endswith(".zip")]
        if not backup_files:
            print("Нет доступных бэкапов для восстановления.")
            return
        
        # Сортируем по дате из имени файла (или по дате изменения) — здесь по имени
        backup_files.sort(reverse=True)  # самый новый будет в начале
        backup_file_name = backup_files[0]  # берём первый (самый свежий)
    
    backup_path = os.path.join(backups_dir, backup_file_name)

    if not os.path.isfile(backup_path):
        print(f"Файл бэкапа не найден: {backup_path}")
        return

    # Распаковка архива
    with zipfile.ZipFile(backup_path, mode="r") as zf:
        # Распаковка прямо в data_dir
        zf.extractall(path=data_dir)

    print(f"Бэкап успешно восстановлен из {backup_path} в {data_dir}")

if __name__ == "__main__":
    # Вызов без параметров попытается найти и распаковать самый новый backup_*.zip
    restore_backup()
