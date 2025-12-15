from collections import defaultdict

def analyze_io(records):
    daily = defaultdict(lambda: {"READ": 0, "WRITE": 0})

    for r in records:
        daily[r["date"]][r["type"]] += 1

    total_ops = sum(
        daily[day]["READ"] + daily[day]["WRITE"]
        for day in daily
    )

    return {
        "daily": daily,
        "total_ops": total_ops
    }
