import threading
import time

def _write_block(block, tracker, penalty=2):
    for _ in range(penalty):
        delay = 0.0002 * len(str(block))
        time.sleep(delay)
        tracker.track_write(delay)
        tracker.total_ops += 1

def _read_block(block, tracker):
    delay = 0.0001
    time.sleep(delay)
    tracker.track_read(delay)
    tracker.total_ops += 1

def run_raid1(records, tracker):
    threads = []
    for r in records:
        if(r["type"]=="READ"):
            t = threading.Thread(target=_write_block, args=(r, tracker))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()
    threads = []
    for r in records:
        if(r["type"]=="WRITE"):
            t = threading.Thread(target=_read_block, args=(r, tracker))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()
