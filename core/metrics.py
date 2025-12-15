import time
from threading import Lock

class PerformanceTracker:
    def __init__(self, total_ops):
        self.total_ops = total_ops
        self.read_time = 0.0
        self.write_time = 0.0
        self.lock = Lock()

    def track_read(self, duration):
        with self.lock:
            self.read_time += duration

    def track_write(self, duration):
        with self.lock:
            self.write_time += duration

    def finalize(self, recovery_time, raid_type):
        total_time = self.read_time + self.write_time + recovery_time
        iops = self.total_ops / total_time if total_time > 0 else 0

        return {
            "RAID Type": raid_type,
            "Read Time": round(self.read_time, 4),
            "Write Time": round(self.write_time, 4),
            "Total IOPS": round(iops, 2)
        }
