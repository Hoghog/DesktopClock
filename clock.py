# Tkinter モジュールをインポートしてコード内で省略可能とする
from tkinter import *
from datetime import datetime

# メインウィンドウ作成
root = Tk()

# メインウィンドウサイズ
root.geometry("720x480")

# メインウィンドウタイトル
root.title("Clock")

# Canvas 作成
c = Canvas(root, bg="#FFFFFF", width=720, height=480)
c.pack(expand=True, fill=BOTH)

# 文字列作成
cd = c.create_text(100, 100, font=('', 40, 'bold'), fill='black')
ct = c.create_text(100, 220, font=('', 120), fill='black')

# メインウィンドウを閉じる
def wm_close():
    root.destroy()

# 閉じるボタン作成
btn = Button(root, text="X", font=('', 16), relief=FLAT, command=wm_close)

# 画面がリサイズされたとき
def change_size(event):
    # 画面の中心座標を取得
    w = c.winfo_width()  / 2
    h = c.winfo_height() / 2

    # 文字列の矩形の中心座標を取得
    cd_coords = c.bbox(cd)
    cd_w = cd_coords[0] + (cd_coords[2] - cd_coords[0]) / 2
    cd_h = cd_coords[1] + (cd_coords[3] - cd_coords[1]) / 2
    ct_coords = c.bbox(ct)
    ct_w = ct_coords[0] + (ct_coords[2] - ct_coords[0]) / 2
    ct_h = ct_coords[1] + (ct_coords[3] - ct_coords[1]) / 2

    # 中心座標を合わせるように移動
    c.move(cd, w - cd_w, h - cd_h - 160)
    c.move(ct, w - ct_w, h - ct_h - 40)
    
    # ボタンの位置を右上に
    btn.place(x=c.winfo_width() - 60, y=24)

# 画面のリサイズをバインドする
root.bind('<Configure>', change_size)

# メインウィンドウの最大化
#root.attributes("-zoom", "1")
root.attributes("-fullscreen", "1")

# 常に最前面に表示
root.attributes("-topmost", True)

def cupdate():
    # 現在時刻を表示
    now = datetime.now()
    d = '{0:0>4d}/{1:0>2d}/{2:0>2d} ({3}.)'.format(now.year, now.month, now.day, now.strftime('%a'))
    t = '{0:0>2d}:{1:0>2d}:{2:0>2d}'.format(now.hour, now.minute, now.second)
    c.itemconfigure(cd, text=d)
    c.itemconfigure(ct, text=t)
    c.update()
    
    # 1秒間隔で繰り返す
    root.after(1000, cupdate)

# コールバック関数を登録
root.after(1000, cupdate)

# メインループ
root.mainloop()
