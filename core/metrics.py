class PerformanceTracker:
    def __init__(self, total_ops):
        self.total_ops = total_ops
        self.read_times = []
        self.write_times = []

    def track_read(self, duration):
        self.read_times.append(duration)

    def track_write(self, duration):
        self.write_times.append(duration)

    def finalize(self, recovery_time, raid_type):
        avg_read = sum(self.read_times) / len(self.read_times) if self.read_times else 0
        avg_write = sum(self.write_times) / len(self.write_times) if self.write_times else 0
        total_time = sum(self.read_times) + sum(self.write_times)
        total_iops = self.total_ops / total_time if total_time > 0 else 0

        return {
            "RAID Type": raid_type,
            "Read Time": round(avg_read, 4),
            "Write Time": round(avg_write, 4),
            "Total IOPS": round(total_iops, 2)
        }
