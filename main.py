from core.log_reader import read_log_file
from core.log_parser import parse_logs
from core.analyzer import analyze_io
from core.metrics import PerformanceTracker
from core.exporter import export_csv

from core.raid.raid1 import run_raid1
from core.raid.raid5 import run_raid5
from core.raid.raid6 import run_raid6
from core.raid.recovery import simulate_failure_and_recovery
try:
    def run_simulation(file_path, raid_type):
        lines = read_log_file(file_path)
        records = parse_logs(lines)
        analysis = analyze_io(records)

        tracker = PerformanceTracker(analysis["total_ops"])

        if raid_type == "RAID1":
            run_raid1(records, tracker)
        elif raid_type == "RAID5":
            run_raid5(records, tracker)
        elif raid_type == "RAID6":
            run_raid6(records, tracker)

        recovery_time, file_size = simulate_failure_and_recovery(records, tracker)

        metrics = tracker.finalize(recovery_time, raid_type)
        export_csv(metrics)

        return metrics, recovery_time, file_size
except Exception as e:
    print("Error:", e)