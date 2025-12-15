from datetime import datetime

def parse_logs(lines):
    records = []

    for line in lines:
        try:
            parts = line.split()
            timestamp = datetime.strptime(
                parts[0] + " " + parts[1], "%Y-%m-%d %H:%M:%S"
            )
            req_type = parts[2].upper()
            response_time = float(parts[3])

            records.append({
                "date": timestamp.date(),
                "type": req_type,
                "response_time": response_time
            })
        except:
            continue

    return records
