from tkinter import Tk, Frame, Label
from datetime import datetime
from PIL import Image, ImageTk
import configparser
import json
import math
import os
import requests
import sys

# このスクリプトの絶対パス
scr_path = os.path.dirname(os.path.abspath(sys.argv[0]))

# 設定ファイルから取得（Python 3.X 用）
inifile=configparser.ConfigParser()
inifile.read(scr_path + "/weather.ini", "UTF-8")

# OpenWeatherMap の情報
KEY = inifile.get("settings", "key")
ZIP = inifile.get("settings", "zip")
URL = inifile.get("settings", "url")

# 天気予報クラス
class Weather(Frame):
    # コンストラクタ
    def __init__(self, master):
        # 親クラスのコンストラクタ
        super().__init__(master, bd=0, bg="white", relief="flat")

        # 地域表示（右寄せ）
        self.wp=Label(self, bg="white", fg="gray", font=("Carlito", 20, "bold"), anchor="e")
        self.wp.grid(row=5, column=0, columnspan=8, padx=20, pady=10, sticky="news")

        # 天候アイコン（ディクショナリー）
        self.icon_dict={
            "01d":Image.open(scr_path + "/img/01d.png"), "01n":Image.open(scr_path + "/img/01n.png"),
            "02d":Image.open(scr_path + "/img/02d.png"), "02n":Image.open(scr_path + "/img/02n.png"),
            "03d":Image.open(scr_path + "/img/03.png"),  "03n":Image.open(scr_path + "/img/03.png"),
            "04d":Image.open(scr_path + "/img/04.png"),  "04n":Image.open(scr_path + "/img/04.png"),
            "09d":Image.open(scr_path + "/img/09.png"),  "09n":Image.open(scr_path + "/img/09.png"),
            "10d":Image.open(scr_path + "/img/10.png"),  "10n":Image.open(scr_path + "/img/10.png"),
            "11d":Image.open(scr_path + "/img/11.png"),  "11n":Image.open(scr_path + "/img/11.png"),
            "13d":Image.open(scr_path + "/img/13.png"),  "13n":Image.open(scr_path + "/img/13.png"),
            "50d":Image.open(scr_path + "/img/50.png"),  "50n":Image.open(scr_path + "/img/50.png")
        }

        # アイコンサイズを画面サイズにフィット（64x64）させる
        for key, value in self.icon_dict.items():
            self.icon_dict[key]=self.icon_dict[key].resize((64, 64), Image.ANTIALIAS)
            self.icon_dict[key]=ImageTk.PhotoImage(self.icon_dict[key])

        # 天気予報（時間帯）
        self.wwl=[
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold")),
            Label(self, text="0", bg="white", font=("Carlito", 30, "bold"))
        ]

        # 天気予報（時間帯）を配置
        for i in range(len(self.wwl)):
            self.wwl[i].grid(row=0, column=i, pady=10, sticky="news")

        # 天気予報（天候）
        self.wwi=[
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white"),
            Label(self, image=self.icon_dict["01d"], bg="white")
        ]

        # 天気予報（天候）を配置
        for i in range(len(self.wwi)):
            self.wwi[i].grid(row=1, column=i, pady=10, sticky="news")

        # 天気予報（気温）
        self.wwt=[
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24)),
            Label(self, text="０°C", bg="white", font=("Carlito", 24))
        ]

        # 天気予報（気温）を配置
        for i in range(len(self.wwt)):
            self.wwt[i].grid(row=2, column=i, pady=10, sticky="news")

        # 天気予報（降水量）
        self.wwr=[
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24)),
            Label(self, text="０mm", bg="white", font=("Carlito", 24))
        ]

        # 天気予報（降水量）を配置
        for i in range(len(self.wwr)):
            self.wwr[i].grid(row=3, column=i, pady=10, sticky="news")

        # 天気予報（風向き）
        self.www=[
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24)),
            Label(self, text="０", bg="white", font=("Carlito", 24))
        ]

        # 天気予報（風向き）を配置
        for i in range(len(self.www)):
            self.www[i].grid(row=4, column=i, pady=10, sticky="news")

        # レイアウト
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        for i in range(len(self.wwl)):
            self.columnconfigure(i, weight=1)

    # 表示を更新
    def update(self):
        # 表示カウンタ
        count=0

        # URL を作成して OpenWeatherMap に問い合わせを行う
        url=URL.format(ZIP, KEY)
        response=requests.get(url)
        forecastData=json.loads(response.text)

        # 結果が得られない場合はエラー終了
        if not ("list" in forecastData):
            self.wp.configure(text="OpenWeatherMap request error!", fg="red")

            # 60秒後にリトライ
            self.master.after(60000, self.update)
            return

        # デバッグ用
        print(forecastData)

        # 結果を 3 時間単位で取得
        for item in forecastData["list"]:
            # 時間帯を 24 時間表記で表示
            forecastDatetime = datetime.fromtimestamp(item["dt"])
            self.wwl[count].configure(text=forecastDatetime.hour)

            # 気候をアイコンで表示
            self.wwi[count].configure(image=self.icon_dict[item["weather"][0]["icon"]])

            # 気温を表示
            self.wwt[count].configure(text="{0}°c".format(round(item["main"]["temp"])))

            # 降水量を表示
            rainfall = 0
            if "rain" in item and "3h" in item["rain"]:
                rainfall = item["rain"]["3h"]
            self.wwr[count].configure(text="{0}mm".format(math.ceil(rainfall)))

            # 風向きを表示
            windspd=item["wind"]["speed"]
            winddeg=item["wind"]["deg"]

            # 風の方角を割り出す
            if winddeg < 22.5:
                # 北旋回
                winddeg += 360

            if winddeg > 337.5 and winddeg < 382.5:
                # 北の風
                self.www[count].configure(text="N, {0}m".format(math.ceil(windspd)))
            elif winddeg > 22.5 and winddeg < 67.5:
                # 北東の風
                self.www[count].configure(text="NE, {0}m".format(math.ceil(windspd)))
            elif winddeg > 67.5 and winddeg < 112.5:
                # 東の風
                self.www[count].configure(text="E, {0}m".format(math.ceil(windspd)))
            elif winddeg > 112.5 and winddeg < 157.5:
                # 南東の風
                self.www[count].configure(text="SE, {0}m".format(math.ceil(windspd)))
            elif winddeg > 157.5 and winddeg < 202.5:
                # 南の風
                self.www[count].configure(text="S, {0}m".format(math.ceil(windspd)))
            elif winddeg > 202.5 and winddeg < 247.5:
                # 南西の風
                self.www[count].configure(text="SW, {0}m".format(math.ceil(windspd)))
            elif winddeg > 247.5 and winddeg < 292.5:
                # 西の風
                self.www[count].configure(text="W, {0}m".format(math.ceil(windspd)))
            elif winddeg > 292.5 and winddeg < 337.5:
                # 北西の風
                self.www[count].configure(text="NW, {0}m".format(math.ceil(windspd)))

            # 表示カウンタを更新
            count += 1

            # 全て表示し終えたらループ終了
            if count >= len(self.wwl):
                # 地域情報を表示
                self.wp.configure(text="{0}, {1} (lat:{2}, lon:{3})".format(
                    forecastData["city"]["country"],
                    forecastData["city"]["name"],
                    forecastData["city"]["coord"]["lat"],
                    forecastData["city"]["coord"]["lon"]), fg="gray")

                # 60秒後に再表示
                self.master.after(60000, self.update)
                return

# 単独処理の場合
def main():
    # メインウィンドウ作成
    root=Tk()

    # メインウィンドウタイトル
    root.title("Weather")

    # メインウィンドウサイズ
    root.geometry("1024x768")

    # メインウィンドウの最大化
    root.attributes("-zoom", "1")

    # 常に最前面に表示
    root.attributes("-topmost", True)

    # メインウィンドウの背景色
    root.configure(bg="white")

    # Weather クラスのインスタンスを生成
    weather=Weather(root)

    # 画面中央に配置
    weather.pack(expand=1, fill="x")

    # 天気予報の更新を開始（update メソッド呼び出し）
    weather.update()

    # メインループ
    root.mainloop()

# import weather による呼び出しでなければ単独処理 main() を実行
if __name__ == "__main__":
    main()
