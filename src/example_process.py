import concurrent.futures
import time

def cpu_bound_task() -> int:
    result = 0
    for i in range(10**8):  # 1億回繰り返す
        result += i % 10
    return result

def main():
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for f in [executor.submit(cpu_bound_task) for _ in range(4)]:
            f.result()
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")

if __name__ == "__main__":
    main()    