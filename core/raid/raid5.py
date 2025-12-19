import threading
import time

def _write_block(block, tracker, penalty=4):
    delay = 0.0002 * len(str(block))
    for _ in range(penalty):
        time.sleep(delay)
        tracker.track_write(delay)
        tracker.total_ops += 1

def _read_block(block, tracker):
    delay = 0.0001
    time.sleep(delay)
    tracker.track_read(delay)
    tracker.total_ops += 1

def xor_block(a, b):
    return bytes(x ^ y for x, y in zip(str(a).encode(), str(b).encode()))

def run_raid5(records, tracker, disks=3):
    stripe_len = disks - 1
    threads = []

    for i in range(0, len(records), stripe_len):
        if(records[i]["type"]=="WRITE"):
            stripe = records[i:i + stripe_len]

            parity = stripe[0]
            for blk in stripe[1:]:
                parity = xor_block(parity, blk)

            for blk in stripe + [parity]:
                t = threading.Thread(target=_write_block, args=(blk, tracker))
                t.start()
                threads.append(t)

    for t in threads:
        t.join()

    threads.clear()
    
    for r in records:
        if(r["type"]=="READ"):
            t = threading.Thread(target=_read_block, args=(r, tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()
