from datetime import datetime, timedelta

def parse_logs(lines):
    records = []

    # start from a fixed base time (for reproducibility)
    base_time = datetime.now()

    for index, line in enumerate(lines):
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        # Alternate READ / WRITE
        io_type = "READ" if index % 2 == 0 else "WRITE"

        # Fixed block size (4KB)
        size = 4096

        # Generate a fake timestamp (1 second apart)
        timestamp = base_time + timedelta(seconds=index)

        records.append({
            "timestamp": timestamp,
            "date": timestamp.date(),
            "type": io_type,
            "size": size
        })

    return records
