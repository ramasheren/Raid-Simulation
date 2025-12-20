import sys
import os
import tempfile
from datetime import datetime

from core.log_reader import read_log_file
from core.log_parser import parse_logs
from core.analyzer import analyze_io
from core.metrics import performance_tracker
from core.exporter import export_csv

from core.raid.raid1 import run_raid1
from core.raid.raid5 import run_raid5
from core.raid.raid6 import run_raid6
from core.raid.recovery import simulate_failure_and_recovery


def run_simulation(file_path, raid_type, disks, step=5):
    lines = read_log_file(file_path)
    records = parse_logs(lines)
    analysis = analyze_io(records)
    tracker = performance_tracker(analysis["total_ops"])

    if raid_type == "RAID1":
        run_raid1(records, tracker)
    elif raid_type == "RAID5":
        run_raid5(records, tracker)
    elif raid_type == "RAID6":
        run_raid6(records, tracker)
        
    def read_write_ratio(records):
        read=0
        write=0
        for r in records:
            if r["type"]=="READ": read+=1 
            else: write+=1
        return f"{read}:{write}"

    ratio = read_write_ratio(records)
    
    recovery_time, file_size = simulate_failure_and_recovery(records, tracker)
    metrics = tracker.finalize(recovery_time, raid_type)

    base = os.path.splitext(os.path.basename(file_path))[0]
    csv_path = os.path.join(
        tempfile.gettempdir(),
        f"raid_performance_{raid_type}_{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )
    export_csv(metrics, csv_path)

    display_metrics = metrics | {"daily_avg": analysis.get("daily_avg", {})}

    sizes, times = [], []
    for size in range(step, len(lines) + 1, step):
        sub_records = parse_logs(lines[:size])
        analysis = analyze_io(sub_records)
        tracker = performance_tracker(analysis["total_ops"])

        if raid_type == "RAID1":
            run_raid1(sub_records, tracker, disks)
        elif raid_type == "RAID5":
            run_raid5(sub_records, tracker, disks)
        elif raid_type == "RAID6":
            run_raid6(sub_records, tracker, disks)

        rt, fs = simulate_failure_and_recovery(sub_records, tracker)
        tracker.finalize(rt, raid_type)

        sizes.append(fs)
        times.append(rt)

    return display_metrics, sizes, times, csv_path, ratio


if __name__ == "__main__":
    if "--ui" in sys.argv:
        from ui.app import launch_ui
        launch_ui()
    else:
        print(run_simulation("sample3.txt", "RAID5")[0])
