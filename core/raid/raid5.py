import time
import threading

def xor_block(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def _write_block(block, tracker):
    start = time.time()
    time.sleep(0.01)
    tracker.track_write(time.time() - start)

def run_raid5(records, tracker, disks=3):
    blocks = [str(r).encode() for r in records]
    threads = []

    for block in blocks:
        t = threading.Thread(target=_write_block, args=(block, tracker))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()