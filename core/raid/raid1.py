import time
import threading

def _write_mirror(block, tracker):
    start = time.time()
    time.sleep(0.001 * len(block))
    tracker.track_write(time.time() - start)

def _read_disk(block, tracker):
    start = time.time()
    time.sleep(0.0005 * len(block))
    tracker.track_read(time.time() - start)

def run_raid1(records, tracker):
    blocks = [str(r).encode() for r in records]
    threads = []

    for block in blocks:
        for _ in range(2):
            t = threading.Thread(target=_write_mirror, args=(block, tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    read_threads = []
    for block in blocks:
        t = threading.Thread(target=_read_disk, args=(block, tracker))
        t.start()
        read_threads.append(t)

    for t in read_threads:
        t.join()

