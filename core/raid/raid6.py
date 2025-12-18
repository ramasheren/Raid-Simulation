import threading
import time

def _write_block(block, tracker, penalty=6):
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

def run_raid6(records, tracker, disks=4):
    stripe_len = disks - 2
    threads = []
    for i in range(0, len(records), stripe_len):
        stripe = records[i:i + stripe_len]
        while len(stripe) < stripe_len:
            stripe.append(0)
        p = stripe[0]
        q = stripe[1] if len(stripe) > 1 else p
        for blk in stripe[2:]:
            p = xor_block(p, blk)
            q = xor_block(q, blk)
        stripe += [p, q]
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
