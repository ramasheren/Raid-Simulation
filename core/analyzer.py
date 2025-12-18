import math
from collections import defaultdict

def analyze_io(records):
    total_reads = 0
    total_writes = 0
    total_ops = 0
    daily_counts = defaultdict(lambda: {"reads": 0, "writes": 0, "ops": 0})

    for rec in records:
        size = rec["size"]
        ops_count =size / 4096
        total_ops += size

        day_counts = daily_counts[rec["date"]]
        day_counts["ops"] += ops_count

        if rec["type"] == "READ":
            total_reads += size
            day_counts["reads"] += size
        else:
            total_writes += size
            day_counts["writes"] += size

    daily_avg = {}
    for day, counts in daily_counts.items():
        avg_read = counts["reads"] / counts["ops"]
        avg_write = counts["writes"] / counts["ops"]
        daily_avg[str(day)] = {
            "avg_read": avg_read,
            "avg_write": avg_write
        }

    return {
        "total_reads": total_reads,
        "total_writes": total_writes,
        "total_ops": total_ops,
        "daily_avg": daily_avg
    }
