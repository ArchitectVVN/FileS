import os
import datetime

def main():
    # 1) Создание структуры директорий
    project_root = "project_root"

    directories = [
        os.path.join(project_root, "data", "raw"),
        os.path.join(project_root, "data", "processed"),
        os.path.join(project_root, "logs"),
        os.path.join(project_root, "backups"),
        os.path.join(project_root, "output")
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # 2) Создание и запись данных в файлы
    # Папка для сохранения файлов
    raw_path = os.path.join(project_root, "data", "raw")

    # Примеры текстов на разных языках и кодировках
    files_info = [
        {
            "filename": "example_utf8.txt",
            "content": "Привет, это текст в UTF-8!", 
            "encoding": "utf-8"
        },
        {
            "filename": "example_iso.txt",
            "content": "Bonjour, c'est du texte en ISO-8859-1!",
            "encoding": "iso-8859-1"
        },
        {
            "filename": "example_ascii.txt",
            "content": "Hello, this is ASCII text!",
            "encoding": "ascii"
        }
    ]

    created_files = []
    for info in files_info:
        file_path = os.path.join(raw_path, info["filename"])
        with open(file_path, mode="w", encoding=info["encoding"]) as f:
            f.write(info["content"])
        created_files.append((file_path, info["encoding"]))

    # 3) Логирование действий в logs/
    logs_path = os.path.join(project_root, "logs")
    log_file_path = os.path.join(logs_path, "creation_log.txt")

    # Формируем текст лога
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = [f"=== Лог создания структуры и файлов: {now_str} ===\n"]
    log_content.append("Созданы (или уже существовали) каталоги:\n")
    for d in directories:
        log_content.append(f"  - {d}\n")
    log_content.append("\nСозданы файлы:\n")
    for fp, enc in created_files:
        log_content.append(f"  - {fp} (encoding={enc})\n")
    log_content.append("\n")

    with open(log_file_path, mode="a", encoding="utf-8") as log_f:
        log_f.writelines(log_content)

    print("Все действия успешно выполнены. Лог записан в", log_file_path)

if __name__ == "__main__":
    main()
