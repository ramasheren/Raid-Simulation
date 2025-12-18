import time
import threading

def xor_block(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def _write_block(block, tracker):
    start = time.time()
    time.sleep(0.01)
    tracker.track_write(time.time() - start)

def _read_block(block, tracker):
    start = time.time()
    time.sleep(0.005)
    tracker.track_read(time.time() - start)

def run_raid6(records, tracker, data_disks=4, parity_disks=2):
    threads = []

    for r in records:
        for _ in range(data_disks + parity_disks):
            t = threading.Thread(target=_write_block, args=(str(r), tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    read_threads = []
    for r in records:
        for _ in range(data_disks + parity_disks):
            t = threading.Thread(target=_read_block, args=(str(r), tracker))
            t.start()
            read_threads.append(t)

    for t in read_threads:
        t.join()
