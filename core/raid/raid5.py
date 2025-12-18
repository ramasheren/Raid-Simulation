import time
import threading

def xor_block(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def _write_block(block, tracker):
    start = time.time()
    time.sleep(0.001 * len(block))
    tracker.track_write(time.time() - start)

def _read_block(block, tracker):
    start = time.time()
    time.sleep(0.0005 * len(block))
    tracker.track_read(time.time() - start)

def run_raid5(records, tracker, disks=3):
    blocks = [str(r).encode() for r in records]
    threads = []

    for i in range(0, len(blocks), disks - 1):
        stripe = blocks[i:i + disks - 1]
        parity = stripe[0]
        for blk in stripe[1:]:
            parity = xor_block(parity, blk)
        stripe.append(parity)
        for blk in stripe:
            t = threading.Thread(target=_write_block, args=(blk, tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    read_threads = []
    for blk in blocks:
        t = threading.Thread(target=_read_block, args=(blk, tracker))
        t.start()
        read_threads.append(t)

    for t in read_threads:
        t.join()
