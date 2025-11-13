import threading
import time


start = time.time()  # 現在時刻（処理開始前）を取得

# うどんを茹でる関数
def boil_udon():

    print("  ◆スレッド:", threading.current_thread().name)
    print('  うどんを茹でます。')
    time.sleep(3)
    print('  うどんが茹であがりました。')

# メイン
if __name__ == "__main__":
    print("◆スレッド:", threading.current_thread().name)
    print('うどんを作ります。')

    # スレッドを作る
    thread1 = threading.Thread(target=boil_udon, name="UdonThread")

    # スレッドの処理を開始
    thread1.start()

    # スレッドの処理を待つ
    thread1.join()

    print('盛り付けます。')
    print('うどんができました。')
end = time.time()  # 現在時刻（処理完了後）を取得

time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する
print(time_diff)  # 処理にかかった時間データを使用