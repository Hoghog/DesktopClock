from tkinter import Tk, Frame, Label
import os
import sys
import time
from datetime import datetime, timedelta
from pytz import timezone
import pymysql.cursors

# MySQL の設定
host="localhost"
user="sensorpi"
password="raspberry"
db="sensor"
charset="utf8mb4"

# センサー表示クラス
class Sensor(Frame):
    # コンストラクタ
    def __init__(self, master):
        # 親クラスのコンストラクタ
        super().__init__(master, bg="white")

        # スペーサ（センサー表示上部の間隔調整）
        self.wsp=Label(self, bg="white")
        self.wsp.pack(pady=20)

        # 温度表示
        self.wst1=Label(self, text="気温", bg="white", font=("Sans", 20, "bold"))
        self.wst1.pack(anchor="e", padx=20, pady=5)

        self.wst2=Label(self, text="-°c", bg="lightblue", font=("Carlito", 40, "bold"))
        self.wst2.pack(anchor="e", padx=20)

        # 湿度表示
        self.wsh1=Label(self, text="湿度", bg="white", font=("Sans", 20, "bold"))
        self.wsh1.pack(anchor="e", padx=20, pady=5)

        self.wsh2=Label(self, text="-%", bg="silver", font=("Carlito", 40, "bold"))
        self.wsh2.pack(anchor="e", padx=20)

        # 気圧表示
        self.wsp1=Label(self, text="気圧", bg="white", font=("Sans", 20, "bold"))
        self.wsp1.pack(anchor="e", padx=20, pady=5)

        self.wsp2=Label(self, text="1013", bg="white", font=("Carlito", 40, "bold"))
        self.wsp2.pack(anchor="e", padx=20)

        # 通信準備中
        self.ser_init=False

    # デストラクタ
    def __del__(self):
        # 通信準備完了の場合
        if self.ser_init:
            # シリアル通信を終了
            self.ser.close()

    # 表示を更新
    def update(self):
        # 現在の時間が30秒のとき
        now=datetime.now(timezone("UTC"))
        if now.second == 30:
            # データベースに接続
            conn=pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db,
                charset=charset,
                cursorclass=pymysql.cursors.DictCursor
            )

            try:
                # データベースに問い合わせる
                with conn.cursor() as cursor:
                    sql  = "SELECT avg_temperature, avg_humidity FROM tbl_serval "
                    sql += "WHERE time > '" + "{0:%Y-%m-%d %H:%M:00}".format(now-timedelta(minutes=1)) + "' "
                    sql += "ORDER BY time DESC"

                    # 温度と湿度を取得
                    cursor.execute(sql)
                    results = cursor.fetchone()

                    # 気温を更新
                    self.wst2.configure(text="{0}°c".format(round(float(results['avg_temperature']))))

                    # 湿度を更新
                    self.wsh2.configure(text="{0}%".format(round(float(results['avg_humidity']))))

            # 例外時
            except:
                # 気温表示を無効化
                self.wst2.configure(text="-°c")

                # 湿度表示を無効化
                self.wsh2.configure(text="-%")

            finally:
                # データベースから切断
                conn.close()

        # 1秒後に再実行
        self.master.after(1000, self.update)

# 単独処理の場合
def main():
    # メインウィンドウ作成
    root=Tk()

    # メインウィンドウタイトル
    root.title("Sensor")

    # メインウィンドウサイズ
    root.geometry("1024x768")

    # メインウィンドウの最大化
    root.attributes("-zoom", "1")

    # 常に最前面に表示
    root.attributes("-topmost", True)

    # メインウィンドウの背景色
    root.configure(bg="white")

    # Sensor クラスのインスタンスを生成
    sensor=Sensor(root)

    # 画面に配置
    sensor.pack(expand=1, fill="y")

    # センサー表示の更新を開始（update メソッド呼び出し）
    sensor.update()

    # メインループ
    root.mainloop()

# import sensor による呼び出しでなければ単独処理 main() を実行
if __name__ == "__main__":
    main()
