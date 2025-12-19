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
        if records[i]["type"] != "WRITE":
            continue

        stripe = records[i:i + stripe_len]     

        stripe += [0] * (stripe_len - len(stripe))
        p, q = stripe[0], stripe[1] 
        
        for blk in stripe[2:]:
            p = xor_block(p, blk)
            q = xor_block(q, blk)

        for blk in stripe + [p, q]:
            t = threading.Thread(target=_write_block, args=(blk, tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    threads.clear()

    for r in records:
        if r["type"] == "READ":
            t = threading.Thread(target=_read_block, args=(r, tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()