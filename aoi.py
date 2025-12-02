import time
import streamlit as st

st.title("⏱ シンプルタイマー")

# 入力：カウントダウンする秒数
seconds = st.number_input("カウントダウン秒数を入力してください", min_value=1, value=10)

# スタートボタン
if st.button("スタート"):
    placeholder = st.empty()

    for remaining in range(seconds, 0, -1):
        placeholder.markdown(f"## ⏳ 残り: {remaining} 秒")
        time.sleep(1)

    placeholder.markdown("## 🎉 タイマー終了！")

