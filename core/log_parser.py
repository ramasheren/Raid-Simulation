from datetime import datetime, timedelta

def parse_logs(lines):
    records = []
    base_time = datetime.now()

    for index, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        io_type = "READ" if index % 2 == 0 else "WRITE"
        size = len(line) 
        timestamp = base_time + timedelta(seconds=index)

        records.append({
            "timestamp": timestamp,
            "date": timestamp.date(),
            "type": io_type,
            "size": size
        })

    return records
