import time
import threading

def _write_mirror(data, tracker):
    start = time.time()
    time.sleep(0.01)
    tracker.track_write(time.time() - start)

def run_raid1(records, tracker):
    threads = []

    for _ in range(2): 
        t = threading.Thread(target=_write_mirror, args=(records, tracker))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
