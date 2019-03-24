from tkinter import Tk, Canvas, Label
from datetime import datetime

# 卓上時計クラス
class Clock(Canvas):
    # コンストラクタ
    def __init__(self, master):
        # 親クラスのコンストラクタ
        super().__init__(master, bg="white")

        # 時刻表示
        self.wt1=Label(self, bg="white", font=("DSEG7 Classic", 140, "bold"))
        self.wt1.grid(row=0, column=0, ipady=50, sticky="news")

        self.wt2=Label(self, bg="white", font=("DSEG7 Classic", 70, "bold"))
        self.wt2.grid(row=0, column=1, ipadx=5, sticky="news")

        # 日付表示
        self.wd=Label(self, bg="white", font=("Carlito", 60, "bold"))
        self.wd.grid(row=1, column=0, columnspan=2, ipady=10, sticky="news")

    # 表示を更新
    def update(self):
        # 現在日時を表示
        now=datetime.now()
        self.wd.configure(text=now.strftime("%Y/%m/%d (%a.)"))
        self.wt1.configure(text=now.strftime("%H:%M"))
        self.wt2.configure(text=now.strftime("%S"))

        # 1秒後に再表示
        self.master.after(1000, self.update)

# 単独処理の場合
def main():
    # メインウィンドウ作成
    root=Tk()

    # メインウィンドウタイトル
    root.title("Clock")

    # メインウィンドウサイズ
    root.geometry("1024x768")

    # メインウィンドウの最大化
    root.attributes("-zoom", "1")

    # 常に最前面に表示
    root.attributes("-topmost", True)

    # メインウィンドウの背景色
    root.configure(bg="white")

    # Clock クラスのインスタンスを生成
    clock=Clock(root)

    # 画面に配置
    clock.pack(expand=1)

    # 時計表示の更新を開始（update メソッド呼び出し）
    clock.update()

    # メインループ
    root.mainloop()

# import clock による呼び出しでなければ単独処理 main() を実行
if __name__ == "__main__":
    main()
