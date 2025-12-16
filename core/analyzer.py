from collections import defaultdict

def analyze_io(records):
    """
    Analyze I/O records to compute totals and daily averages.
    Each record must have 'date', 'type', 'size'.
    """
    total_reads = 0
    total_writes = 0
    daily_counts = defaultdict(lambda: {"reads": 0, "writes": 0})

    for rec in records:
        if rec["type"] == "READ":
            total_reads += rec["size"]
            daily_counts[rec["date"]]["reads"] += rec["size"]
        elif rec["type"] == "WRITE":
            total_writes += rec["size"]
            daily_counts[rec["date"]]["writes"] += rec["size"]

    # Compute daily averages
    daily_avg = {}
    for day, counts in daily_counts.items():
        daily_avg[str(day)] = {
            "avg_read": counts["reads"],
            "avg_write": counts["writes"]
        }

    total_ops = total_reads + total_writes

    return {
        "total_reads": total_reads,
        "total_writes": total_writes,
        "total_ops": total_ops,
        "daily_avg": daily_avg
    }
