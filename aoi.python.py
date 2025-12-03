import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="柔道アプリ", layout="wide")
st.title("🥋 柔道 練習管理 & 試合分析アプリ")

# 保存するCSV
PRACTICE_FILE = "practice.csv"
MATCH_FILE = "match.csv"

# CSVの読み込み（なければ空で作成）
if os.path.exists(PRACTICE_FILE):
    practice = pd.read_csv(PRACTICE_FILE)
else:
    practice = pd.DataFrame(columns=["日付", "練習時間(分)", "技", "乱取り本数", "勝率", "コンディション"])

if os.path.exists(MATCH_FILE):
    match = pd.read_csv(MATCH_FILE)
else:
    match = pd.DataFrame(columns=["日付", "大会名", "相手", "技", "決まり手", "時間(秒)", "反則"])


# タブ
tab1, tab2, tab3 = st.tabs(["🏋 練習管理", "🥋 試合分析", "📊 パフォーマンス統計"])


# ＝＝＝＝＝＝＝＝＝＝ 練習管理 ＝＝＝＝＝＝＝＝＝＝
with tab1:
    st.header("🏋 練習記録の追加")

    with st.form("practice_form"):
        col1, col2 = st.columns(2)
        with col1:
            p_date = st.date_input("日付")
            p_time = st.number_input("練習時間（分）", 0)
            p_tech = st.text_input("練習した技")
        with col2:
            p_randori = st.number_input("乱取り本数", 0)
            p_win = st.slider("勝率（%）", 0, 100, 50)
            p_cond = st.slider("コンディション（1〜10）", 1, 10, 5)

        p_btn = st.form_submit_button("保存")

    if p_btn:
        new = pd.DataFrame([[p_date, p_time, p_tech, p_randori, p_win, p_cond]],
                           columns=practice.columns)
        practice = pd.concat([practice, new], ignore_index=True)
        practice.to_csv(PRACTICE_FILE, index=False)
        st.success("保存しました！")

    st.subheader("📌 練習の履歴")
    st.dataframe(practice, use_container_width=True)

    if not practice.empty:
        st.subheader("📈 練習時間の推移")
        st.line_chart(practice["練習時間(分)"])


# ＝＝＝＝＝＝＝＝＝＝ 試合分析 ＝＝＝＝＝＝＝＝＝＝
with tab2:
    st.header("🥋 試合記録の追加")

    with st.form("match_form"):
        m_date = st.date_input("日付", key="m_date")
        m_tour = st.text_input("大会名")
        m_opp = st.text_input("相手")
        m_tech = st.text_input("決めた技")
        m_type = st.selectbox("決まり手", ["一本", "技あり", "判定"])
        m_time = st.number_input("試合時間（秒）", 0)
        m_foul = st.selectbox("反則", ["なし", "指導", "反則負け"])

        m_btn = st.form_submit_button("保存")

    if m_btn:
        new = pd.DataFrame([[m_date, m_tour, m_opp, m_tech, m_type, m_time, m_foul]],
                           columns=match.columns)
        match = pd.concat([match, new], ignore_index=True)
        match.to_csv(MATCH_FILE, index=False)
        st.success("保存しました！")

    st.subheader("📌 試合の履歴")
    st.dataframe(match, use_container_width=True)

    if not match.empty:
        st.subheader("🥋 決め技ランキング")
        st.bar_chart(match["技"].value_counts())


# ＝＝＝＝＝＝＝＝＝＝ パフォーマンス統計 ＝＝＝＝＝＝＝＝＝＝
with tab3:
    st.header("📊 練習 × 試合の関係分析")

    if practice.empty or match.empty:
        st.warning("練習データと試合データの両方を登録してください！")
    else:
        st.subheader("🟠 練習時間 × 勝率")
        st.scatter_chart(practice, x="練習時間(分)", y="勝率")

        st.subheader("🔵 コンディション × 勝率")
        st.scatter_chart(practice, x="コンディション", y="勝率")
