import threading

def _write_block(record, tracker, penalty=6):
    for _ in range(penalty):
        delay = 0.0002 * len(str(record))
        tracker.track_write(delay)
        tracker.total_ops += 1

def _read_block(record, tracker):
    delay = 0.0001
    tracker.track_read(delay)
    tracker.total_ops += 1

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def run_raid6(records, tracker, disks=10):
    usable = max(1, disks - 2)  
    threads = []
    disk_blocks = [[] for _ in range(disks)]

    def worker(tid):
        for i, record in enumerate(records):
            if i % usable != tid:
                continue

            stripe_index = i // usable
            parity_disk_p = stripe_index % disks
            parity_disk_q = (parity_disk_p + 1) % disks
            data_disk = i % usable
            if data_disk >= parity_disk_p:
                data_disk += 1
            if data_disk >= parity_disk_q:
                data_disk += 1

            block = record["data"].encode() if "data" in record else b""

            if record["type"] == "READ":
                _read_block(record, tracker)
            elif record["type"] == "WRITE":
                # write data
                disk_blocks[data_disk].append(block)
                _write_block(record, tracker)

                data_blocks = [disk_blocks[d][-1] for d in range(disks)
                               if d != parity_disk_p and d != parity_disk_q and disk_blocks[d]]
                if data_blocks:
                    parity_p = data_blocks[0]
                    for blk in data_blocks[1:]:
                        parity_p = xor_bytes(parity_p, blk)
                    disk_blocks[parity_disk_p].append(parity_p)
                    _write_block(record, tracker)

                    parity_q = bytes(((b + 1) % 256) for b in parity_p) 
                    disk_blocks[parity_disk_q].append(parity_q)
                    _write_block(record, tracker)

    for tid in range(usable):
        t = threading.Thread(target=worker, args=(tid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
