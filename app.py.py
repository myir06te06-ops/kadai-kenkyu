import streamlit as st
from datetime import date
import os
import csv

# CSVファイル名
FILE_NAME = "log.csv"

# CSV読み込み
def load_logs():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)

# 今日のログ
def get_today_log(logs):
    today = date.today().strftime("%Y-%m-%d")
    for r in logs:
        if r[0] == today:
            return r[1]
    return None

# ログ保存
def save_log(status):
    logs = load_logs()
    today = date.today().strftime("%Y-%m-%d")
    found = False
    new_logs = []
    for r in logs:
        if r[0] == today:
            new_logs.append([today, status])
            found = True
        else:
            new_logs.append(r)
    if not found:
        new_logs.append([today, status])
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(new_logs)

# ---------- Web UI ----------
st.title("生活見守りアプリ（Web版）")

logs = load_logs()
today_status = get_today_log(logs)

st.write("### 今日の操作記録：", today_status if today_status else "未入力")

col1, col2, col3 = st.columns(3)

if not today_status:
    with col1:
        if st.button("元気"):
            save_log("元気")
            st.experimental_rerun()
    with col2:
        if st.button("普通"):
            save_log("普通")
            st.experimental_rerun()
    with col3:
        if st.button("不調"):
            save_log("不調")
            st.experimental_rerun()
else:
    st.warning("今日の記録はもう入力済みです。")

st.write("---")
st.write("#### 過去の記録")
for r in logs:
    st.write(f"{r[0]} : {r[1]}")
