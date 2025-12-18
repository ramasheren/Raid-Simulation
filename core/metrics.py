class performance_tracker:
    def __init__(self, total_ops: int = 0):
        self.total_ops = total_ops
        self.read_times = 0.0
        self.write_times = 0.0

    def track_read(self, duration: float):
        self.read_times += duration
        self.total_ops += 1

    def track_write(self, duration: float):
        self.write_times += duration
        self.total_ops += 1

    def finalize(self, recovery_time: float, raid_type: str) -> dict:
        total_time = self.read_times + self.write_times
        total_iops = self.total_ops / total_time if total_time > 0 else 0
        return {
            "RAID Type": raid_type,
            "Read Time": round(self.read_times, 4),
            "Write Time": round(self.write_times, 4),
            "Total IOPS": round(total_iops, 2)
        }
