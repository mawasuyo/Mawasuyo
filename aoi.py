import streamlit as st

st.title("電卓アプリ")

# 入力
num1 = st.number_input("1つ目の数値を入力", value=0.0)
num2 = st.number_input("2つ目の数値を入力", value=0.0)

# 演算選択
operation = st.selectbox(
    "演算を選択してください",
    ["足し算 (+)", "引き算 (-)", "掛け算 (×)", "割り算 (÷)"]
)

# ボタン
if st.button("計算する"):
    if operation == "足し算 (+)":
        result = num1 + num2
    elif operation == "引き算 (-)":
        result = num1 - num2
    elif operation == "掛け算 (×)":
        result = num1 * num2
    elif operation == "割り算 (÷)":
        if num2 == 0:
            st.error("0で割ることはできません。")
            st.stop()
        result = num1 / num2

    st.success(f"結果：**{result}**")

