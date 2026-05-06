from .client.baby_redis_client import BabyRedisClient
import threading
import time

num_threads = 150
ITERATIONS_PER_THREAD = 100

success_count = 0
error_count = 0
lock = threading.Lock()

def worker(client_id):
    global success_count, error_count
    client = BabyRedisClient()
    try:
        for i in range(ITERATIONS_PER_THREAD):
            key = f"key:{client_id}:{i}"
            value = f"value:{client_id}:{i}"
            try:
                client.set(key, value)
                got = client.get(key)
                if got != value:
                    with lock:
                        error_count += 1
                    if i % 10 == 0:
                        print(f"[Thread {client_id}] mismatch at i={i}: got={got!r}")
                    continue
                client.delete(key)
                with lock:
                    success_count += 1
                if i % 10 == 0:
                    print(f"[Thread {client_id}] progress i={i}")
            except Exception as e:
                with lock:
                    error_count += 1
                print(f"[Thread {client_id}] error at i={i}: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    threads = []
    start_time = time.time()

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    total_ops = num_threads * ITERATIONS_PER_THREAD

    print(f"Total operations attempted: {total_ops}")
    print(f"Successful operations:      {success_count}")
    print(f"Failed operations:          {error_count}")
    print(f"Stress test completed in {end_time - start_time:.2f} seconds.")
    print("All good?" if error_count == 0 else "There were errors.")
