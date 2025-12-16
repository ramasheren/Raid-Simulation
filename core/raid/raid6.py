import time
import threading

def _write_block(block, tracker):
    start = time.time()
    time.sleep(0.015)
    tracker.track_write(time.time() - start)

def run_raid6(records, tracker):
    threads = []

    for r in records:
        t = threading.Thread(target=_write_block, args=(r, tracker))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()