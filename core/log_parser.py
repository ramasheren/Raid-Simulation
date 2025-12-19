from datetime import datetime, timedelta
import random

def parse_logs(lines):
    records = []
    base_time = datetime.now()

    for index, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        rand_val = random.randint(1,2)
        io_type = "READ" if rand_val == 1 else "WRITE"
        size = len(line) 
        timestamp = base_time + timedelta(seconds=index)

        records.append({
            "timestamp": timestamp,
            "date": timestamp.date(),
            "type": io_type,
            "size": size
        })

    return records
