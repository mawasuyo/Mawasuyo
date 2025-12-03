import streamlit as st

st.title("柔道アプリ（練習管理 × 試合分析）🥋")

menu = st.sidebar.selectbox("メニューを選択", ["ホーム", "練習記録", "試合分析"])

if menu == "ホーム":
    st.write("左のメニューから機能を選んでください🔥")

elif menu == "練習記録":
    st.header("📌 練習記録")
    date = st.date_input("日付")
    menu_type = st.text_input("練習メニュー")
    minutes = st.number_input("練習時間（分）", 0)
    note = st.text_area("メモ")
    if st.button("保存"):
        st.success("保存しました！")

elif menu == "試合分析":
    st.header("🎯 試合分析")
    opponent = st.text_input("相手の名前")
    score = st.text_input("勝敗 or スコア")
    success = st.text_input("成功した技・形")
    bad = st.text_input("課題・改善点")
    if st.button("保存"):
        st.success("保存しました！")

