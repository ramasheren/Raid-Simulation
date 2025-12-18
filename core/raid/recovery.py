import time
import threading

def _recover_worker():
    time.sleep(0.02)

def simulate_failure_and_recovery(records, tracker):
    start = time.time()
    threads = []

    workers = max(1, len(records) // 5)

    for _ in range(workers):
        t = threading.Thread(target=_recover_worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    recovery_time = time.time() - start
    tracker.track_read(recovery_time)

    return recovery_time, len(records)
