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

def run_raid6(records, tracker, data_disks=4, parity_disks=2):
    threads = []

    for r in records:
        data_blocks = [str(r)] * data_disks
        parity_blocks = [str(r)] * parity_disks

        for block in data_blocks:
            t = threading.Thread(target=_write_block, args=(block, tracker))
            t.start()
            threads.append(t)

        parity = bytes([0] * len(str(r)))
        for block in data_blocks:
            parity = xor_block(parity, block.encode())

        for block in parity_blocks:
            t = threading.Thread(target=_write_block, args=(parity, tracker))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    read_threads = []
    for r in records:
        all_blocks = [str(r)] * (data_disks + parity_disks)
        for block in all_blocks:
            t = threading.Thread(target=_read_block, args=(block, tracker))
            t.start()
            read_threads.append(t)

    for t in read_threads:
        t.join()
