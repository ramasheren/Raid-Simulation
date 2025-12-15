import csv
import os

def export_csv(metrics, filename="raid_performance.csv"):
    exists = os.path.exists(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["RAID Type", "Read Time", "Write Time", "Total IOPS"]
        )

        if not exists:
            writer.writeheader()

        writer.writerow(metrics)
