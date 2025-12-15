import time
import threading

def _recover_block(tracker):
    start = time.time()
    time.sleep(0.02)
    tracker.track_read(time.time() - start)

def simulate_failure_and_recovery(records, tracker):
    start = time.time()
    threads = []

    for _ in range(len(records) // 5 + 1):
        t = threading.Thread(target=_recover_block, args=(tracker,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    recovery_time = time.time() - start
    file_size = len(records)

    return recovery_time, file_size
