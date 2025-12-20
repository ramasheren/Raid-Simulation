import threading

def _write_block(record, tracker, penalty=2):
    for _ in range(penalty):
        delay = 0.0002 * len(str(record))
        tracker.track_write(delay)
        tracker.total_ops += 1

def _read_block(record, tracker):
    delay = 0.0001
    tracker.track_read(delay)
    tracker.total_ops += 1

def run_raid1(records, tracker, disks=10):
    usable = max(1, disks // 2) 
    threads = []

    def worker(tid):
        for i, record in enumerate(records):
            if i % usable != tid:
                continue
            if record["type"] == "READ":
                _read_block(record, tracker)
            elif record["type"] == "WRITE":
                _write_block(record, tracker)

    for tid in range(usable):
        t = threading.Thread(target=worker, args=(tid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
