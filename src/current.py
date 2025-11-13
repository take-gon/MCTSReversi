import threading
import time
import os

# def worker():
#     t = threading.current_thread()
#     print(f"実行中のスレッド: {t.name}, ID: {t.ident}")
#     print(f"{threading.current_thread().name} のCPU割当:", os.sched_getaffinity(0))

# # メインスレッド
# print(f"メインスレッド: {threading.current_thread().name}")

# # ワーカースレッドを2つ起動
# for i in range(10):
#     th = threading.Thread(target=worker, name=f"Worker-{i}")
#     th.start()

# import threading
# import time
# import os

import threading
import time
from cpu_now import get_current_cpu

def worker(i, secs=2.0):
    t = threading.current_thread()
    start = time.time()
    while time.time() - start < secs:
        core = get_current_cpu()
        print(f"Worker-{i} (id={t.ident}, tid={t.native_id}) -> CPU{core}")
        time.sleep(0.1)
    print(f"Worker-{i} done")

print(f"Main: {threading.current_thread().name}")
threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for th in threads: th.start()
for th in threads: th.join()
