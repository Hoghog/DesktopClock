from tkinter import Tk, Frame, Label

# センサー表示クラス
class Sensor(Frame):
    # コンストラクタ
    def __init__(self, master):
        # 親クラスのコンストラクタ
        super().__init__(master, bg="white")

        # スペーサ（センサー表示上部の間隔調整）
        self.wsp=Label(self, bg="white")
        self.wsp.grid(row=0, column=0, ipady=84, sticky="news")

        # 温度表示
        self.wst1=Label(self, text="気温：", bg="white", font=("", 20, "bold"))
        self.wst1.grid(row=1, column=0, pady=5, sticky="news")

        self.wst2=Label(self, text="0°c", bg="lightblue", font=("", 30, "bold"))
        self.wst2.grid(row=1, column=1, ipadx=5, pady=5, sticky="news")

        # 湿度表示
        self.wsh1=Label(self, text="湿度：", bg="white", font=("", 20, "bold"))
        self.wsh1.grid(row=2, column=0, pady=5, sticky="news")

        self.wsh2=Label(self, text="0%", bg="silver", font=("", 30, "bold"))
        self.wsh2.grid(row=2, column=1, ipadx=5, pady=5, sticky="news")

        # 気圧表示
        self.wsp1=Label(self, text="気圧：1013", bg="white", font=("", 20, "bold"))
        self.wsp1.grid(row=3, column=0, columnspan=2, pady=5, sticky="news")

    # 表示を更新
    def update(self):
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
