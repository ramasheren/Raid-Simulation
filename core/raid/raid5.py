import threading

def _write_block(record, tracker, penalty=4):
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

def run_raid5(records, tracker, disks=10):
    usable = max(1, disks - 1)  
    threads = []
    disk_blocks = [[] for _ in range(disks)]

    def worker(tid):
        for i, record in enumerate(records):
            if i % usable != tid:
                continue

            stripe_index = i // usable
            parity_disk = stripe_index % disks
            data_disk = i % usable
            if data_disk >= parity_disk:
                data_disk += 1

            block = record["data"].encode() if "data" in record else b""

            if record["type"] == "READ":
                _read_block(record, tracker)
            elif record["type"] == "WRITE":
                # write data
                disk_blocks[data_disk].append(block)
                _write_block(record, tracker)

                data_blocks = [disk_blocks[d][-1] for d in range(disks) if d != parity_disk and disk_blocks[d]]
                if data_blocks:
                    parity_block = data_blocks[0]
                    for blk in data_blocks[1:]:
                        parity_block = xor_bytes(parity_block, blk)
                    disk_blocks[parity_disk].append(parity_block)
                    _write_block(record, tracker) 

    for tid in range(usable):
        t = threading.Thread(target=worker, args=(tid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()