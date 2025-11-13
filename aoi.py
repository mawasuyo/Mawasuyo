import streamlit as st
import random

st.title("🔮 今日の運勢 占いアプリ 🔮")

name = st.text_input("あなたの名前を教えてね：")

if name:
    answers = [
        "ましだな",
        "ふつー",
        "今日ちょっとやべーぞ",
        "死んだ方がいいかも"
    ]

    result = random.choice(answers)
    st.write("🔮 占いの結果 🔮")
    st.write(f"{name} さんの今日の運勢は… {result}")