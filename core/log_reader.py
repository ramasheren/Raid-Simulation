def read_log_file(file_path):
    file_path = str(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
