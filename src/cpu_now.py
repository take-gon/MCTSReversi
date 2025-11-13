# cpu_now.py
import threading
import sys

def get_current_cpu():
    # 1) まずは標準の os.sched_getcpu() を試す（あれば一番簡単）
    try:
        import os
        return os.sched_getcpu()
    except Exception:
        pass

    # 2) Linux (glibc) なら libc の sched_getcpu() を ctypes で直接叩く
    if sys.platform.startswith("linux"):
        try:
            import ctypes
            libc = ctypes.CDLL("libc.so.6")
            libc.sched_getcpu.restype = ctypes.c_int
            cpu = libc.sched_getcpu()
            if cpu >= 0:
                return cpu
        except Exception:
            pass

        # 3) それでもダメなら /proc/self/task/<tid>/stat の 39番目フィールドを読む
        #    （直近で実行していたCPU番号）
        try:
            tid = threading.get_native_id()  # Python 3.8+
            with open(f"/proc/self/task/{tid}/stat") as f:
                fields = f.read().split()
                # fields[38] が "processor"（0始まりで39番目）
                return int(fields[38])
        except Exception:
            pass

    # 4) Windows: GetCurrentProcessorNumber()
    if sys.platform.startswith("win"):
        try:
            import ctypes
            return ctypes.windll.kernel32.GetCurrentProcessorNumber()
        except Exception:
            pass

    # 5) どうしても取得できない環境では None を返す
    return None
