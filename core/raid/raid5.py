import threading
import time

def _write_block(block, tracker, penalty=4):
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

def xor_block(a, b):
    a, b = str(a).encode(), str(b).encode()
    return bytes(x ^ y for x, y in zip(a, b))

def run_raid5(records, tracker, disks=3):
    stripe_len = disks - 1
    threads = []
    for i in range(0, len(records), stripe_len):
        stripe = records[i:i + stripe_len]
        parity = stripe[0] if stripe else 0
        for blk in stripe[1:]:
            parity = xor_block(parity, blk)
        stripe.append(parity)
        for blk in stripe:
            t = threading.Thread(target=_write_block, args=(blk, tracker))
            t.start()
            threads.append(t)
    for t in threads:
        t.join()
    threads = []
    for r in records:
        t = threading.Thread(target=_read_block, args=(r, tracker))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
