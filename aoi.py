import streamlit as st
import random

st.title("🔮 今日の運勢 占いアプリ 🔮")

name = st.text_input("あなたの名前を教えてね：")

if name:
    answers = [
        "うんこ",
        "ちんこ",
        "おしっこ",
        "げり"
    ]

    result = random.choice(answers)
    st.write("🔮 占いの結果 🔮")
    st.write(f"{name} さんの今日の運勢は… {result}")