from tkinter import Tk, Frame, Label
import os
import sensor_setting
import serial
import sys
import time

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
        # センサーデバイスを探す
        dev=sensor_setting.dev_search()

        try:
            # 通信準備中かつ、センサーデバイスが OS に認識されている場合
            if not self.ser_init and dev!="":
                # シリアル通信の初期化
                self.ser=serial.Serial(dev, sensor_setting.bps, timeout=sensor_setting.timeout)

                # 通信準備完了
                self.ser_init=True

        # 例外時は何もしない
        except:
            pass

        # 通信準備完了かつ、認識されていない場合
        if dev=="" and self.ser_init:
            # シリアル通信を終了
            self.ser.close()

            # 通信準備中
            self.ser_init=False

        try:
            # シリアル通信を開始
            if self.ser.is_open==False:
                self.ser.open()

            # 1行受信（b'気温,湿度¥r¥n' の形式で受信）
            serval=self.ser.readline(self.ser.inWaiting())

            if not serval=="":
                # 改行コードを削除（b'気温,湿度'）
                serval=serval.strip()

                # バイナリ形式から文字列に変換（気温,湿度）
                serval=serval.decode("utf-8")

                # CSV を分割
                serary=serval.split(",")
                print(serval)
                # 気温を更新
                self.wst2.configure(text="{0}°c".format(round(float(serary[0]))))

                # 湿度を更新
                self.wsh2.configure(text="{0}%".format(round(float(serary[1]))))

        # 例外時
        except:
            # 気温表示を無効化
            self.wst2.configure(text="-°c")

            # 湿度表示を無効化
            self.wsh2.configure(text="-%")

        # 1秒後に再表示
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
