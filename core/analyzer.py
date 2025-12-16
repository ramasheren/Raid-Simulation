# core/analyzer.py

def analyze_io(records):
    """Analyze I/O records to calculate totals and averages."""
    total_reads = sum(r["size"] for r in records if r["type"] == "READ")
    total_writes = sum(r["size"] for r in records if r["type"] == "WRITE")
    total_ops = len(records)

    avg_reads = total_reads / total_ops if total_ops else 0
    avg_writes = total_writes / total_ops if total_ops else 0
    avg_io = (total_reads + total_writes) / total_ops if total_ops else 0

    return {
        "total_reads": total_reads,
        "total_writes": total_writes,
        "total_ops": total_ops,
        "avg_reads": avg_reads,
        "avg_writes": avg_writes,
        "avg_io": avg_io,
    }
