from collections import defaultdict

def analyze_io(records):
    total_reads = 0
    total_writes = 0
    total_ops = 0
    daily_counts = defaultdict(lambda: {"reads": 0, "writes": 0, "ops": 0})

    for rec in records:
        size = rec["size"]
        total_ops += size
        daily_counts[rec["date"]]["ops"] += size

        if rec["type"] == "READ":
            total_reads += size
            daily_counts[rec["date"]]["reads"] += size
        elif rec["type"] == "WRITE":
            total_writes += size
            daily_counts[rec["date"]]["writes"] += size

    daily_avg = {}
    for day, counts in daily_counts.items():
        num_ops = counts["ops"] or 1
        daily_avg[str(day)] = {
            "avg_read": counts["reads"] / (num_ops / 4096),
            "avg_write": counts["writes"] / (num_ops / 4096)
        }

    return {
        "total_reads": total_reads,
        "total_writes": total_writes,
        "total_ops": total_ops,
        "daily_avg": daily_avg
    }
