import tkinter as tk
import tkinter.messagebox as msg
from datetime import date
import os
import csv

# ------------------------------
# ファイルパス取得（デスクトップ）
# ------------------------------
def get_desktop_folder():
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
        desktop = winreg.QueryValueEx(key, "Desktop")[0]
        desktop = desktop.replace("%USERPROFILE%", os.environ["USERPROFILE"])
        return desktop
    except:
        return os.path.join(os.environ["USERPROFILE"], "Desktop")

FILE_NAME = os.path.join(get_desktop_folder(), "log.csv")

# ------------------------------
# 端末ID取得
# ------------------------------
TERMINAL_ID = os.environ.get("COMPUTERNAME", "UnknownPC")

# ------------------------------
# 保存関数
# ------------------------------
def save_today(status):
    today_str = date.today().strftime("%Y-%m-%d")

    # 既存データを読み込む
    existing_rows = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            existing_rows = list(csv.reader(f))

    # 今日かつ自分の端末IDの行があれば置き換え、なければ追加
    new_rows = []
    found = False
    for r in existing_rows:
        if r[0] == today_str and r[1] == TERMINAL_ID:
            new_rows.append([today_str, TERMINAL_ID, status])
            found = True
        else:
            new_rows.append(r)
    if not found:
        new_rows.append([today_str, TERMINAL_ID, status])

    # CSVに書き込む
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    status_label.config(text=f"今日の操作記録：{status}")
    msg.showinfo("保存完了", f"{status} を記録しました！")

    # ボタン無効化
    for b in buttons:
        b.config(state="disabled")
    edit_btn.config(state="normal")

# ------------------------------
# 今日の端末の入力をチェック
# ------------------------------
def check_today():
    if not os.path.exists(FILE_NAME):
        return None
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
        for r in rows:
            if r[0] == date.today().strftime("%Y-%m-%d") and r[1] == TERMINAL_ID:
                return r[2]
    return None

# ------------------------------
# 編集ボタン
# ------------------------------
def edit_today():
    if msg.askyesno("編集", "今日の記録を変更してもいいですか？"):
        for b in buttons:
            b.config(state="normal")
        status_label.config(text="今日の操作記録：未入力")
        edit_btn.config(state="disabled")

# ------------------------------
# ボタン押下時
# ------------------------------
def on_status(status):
    save_today(status)

# ------------------------------
# GUI構築
# ------------------------------
root = tk.Tk()
root.title("生活見守りアプリ")
root.geometry("500x620")

title = tk.Label(root, text="生活見守りアプリ", font=("Arial", 22))
title.pack(pady=10)

status_label = tk.Label(root, text="今日の操作記録：未入力", font=("Arial", 22))
status_label.pack(pady=8)

# 今日の自分端末の記録をチェック
today_status = check_today()
if today_status:
    status_label.config(text=f"今日の操作記録：{today_status}")

buttons = []
for text in ["元気", "普通", "不調"]:
    btn = tk.Button(
        root,
        text=text,
        font=("Meiryo", 23),
        width=8,
        height=2,
        command=lambda s=text: on_status(s)
    )
    btn.pack(pady=6)
    buttons.append(btn)

# 今日すでに押していたら無効化
if today_status:
    for b in buttons:
        b.config(state="disabled")

# 編集ボタン
edit_btn = tk.Button(
    root,
    text="今日の記録を編集する",
    font=("Arial", 18),
    bg="lightblue",
    command=edit_today
)
edit_btn.pack(pady=14)

if not today_status:
    edit_btn.config(state="disabled")

root.mainloop()
