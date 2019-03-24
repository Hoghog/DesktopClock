from tkinter import *
import tkinter.ttk as ttk
from clock import Clock
from sensor import Sensor
from weather import Weather

# MainFrame クラス
class MainFrame(ttk.Frame):
    # コンストラクタ
    def __init__(self, master=None, *args, **kwargs):
        # 親クラスのコンストラクタ
        super().__init__(args, **kwargs)

        # Clock クラスのインスタンスを生成して配置
        self.clock=Clock(self)
        self.clock.grid(row=0, column=0, sticky="news")

        # Sensor クラスのインスタンスを生成して配置
        self.sensor=Sensor(self)
        self.sensor.grid(row=0, column=1, sticky="news")

        # Weather クラスのインスタンスを生成して配置
        self.weather=Weather(self)
        self.weather.grid(row=1, column=0, columnspan=2, sticky="news")

        # レイアウト
        self.columnconfigure(1, weight=1)

    def update(self):
        # 時計表示の更新を開始（Clock.update メソッド呼び出し）
        self.clock.update()

        # センサー表示の更新を開始（Sensor.update メソッド呼び出し）
        self.sensor.update()

        # 天気予報の更新を開始（Weather.update メソッド呼び出し）
        self.weather.update()

# メインウィンドウ作成
root=Tk()

# メインウィンドウタイトル
root.title("Main")

# メインウィンドウサイズ
root.geometry("1024x768")

# メインウィンドウの最大化
#root.attributes("-zoom", "1")
root.attributes("-fullscreen", "1")

# 常に最前面に表示
root.attributes("-topmost", True)

# メインウィンドウの背景色
root.configure(bg="white")

# メインフレームを配置
app=MainFrame(root)

# 画面に配置
app.pack(fill="both")

# 閉じるボタン作成
close=Button(root, text=" X ", font=("Carlito", 16, "bold"), relief=FLAT, command=root.destroy)

# 画面がリサイズされたとき、ボタンの位置を右上に移動
def change_size(event):
    close.place(x=root.winfo_width() - 60, y=14)

# 画面のリサイズをバインドする
root.bind('<Configure>', change_size)

# MainFrame.update メソッドを呼び出す
app.update()

# メインループ
root.mainloop()
