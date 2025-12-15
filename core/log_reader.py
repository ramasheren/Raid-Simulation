def read_log_file(file_path):
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
    return lines
