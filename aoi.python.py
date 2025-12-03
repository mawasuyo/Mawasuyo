import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="柔道 練習＆試合分析アプリ", layout="wide")
st.title("🥋 柔道 練習＆試合分析アプリ")

# CSVファイルのパス
PRACTICE_CSV = "practice.csv"
MATCH_CSV = "match.csv"

# CSVの読み込み（初回は空データで作成）
if os.path.exists(PRACTICE_CSV):
    practice_df = pd.read_csv(PRACTICE_CSV)
else:
    practice_df = pd.DataFrame(columns=["日付", "練習時間(分)", "技", "乱取り本数", "勝率", "コンディション"])

if os.path.exists(MATCH_CSV):
    match_df = pd.read_csv(MATCH_CSV)
else:
    match_df = pd.DataFrame(columns=["日付", "大会名", "相手", "技", "決まり手", "時間(秒)", "反則"])

# =============================
# タブ設定
# =============================
tab1, tab2, tab3, tab4 = st.tabs(["🏋 練習管理", "🥋 試合分析", "📊 パフォーマンス統計", "📁 保存データ確認"])


# ============ 練習管理 ============
with tab1:
    st.header("🏋 練習記録を登録")

    with st.form("practice_form"):
        date = st.date_input("日付")
        time = st.number_input("練習時間（分）", min_value=0)
        technique = st.text_input("練習した技")
        randori = st.number_input("乱取り本数", min_value=0)
        win_rate = st.slider("乱取り勝率（%）", 0, 100, 50)
        condition = st.slider("コンディション（1〜10）", 1, 10, 5)
        submit = st.form_submit_button("追加")

    if submit:
        new_data = pd.DataFrame([[date, time, technique, randori, win_rate, condition]],
                                columns=practice_df.columns)
        practice_df = pd.concat([practice_df, new_data], ignore_index=True)
        practice_df.to_csv(PRACTICE_CSV, index=False)
        st.success("保存しました！")

    st.subheader("📌 練習履歴")
    st.dataframe(practice_df, use_container_width=True)

    if not practice_df.empty:
        st.subheader("📈 練習時間の推移")
        st.line_chart(practice_df["練習時間(分)"])


# ============ 試合分析 ============
with tab2:
    st.header("🥋 試合記録を登録")

    with st.form("match_form"):
        mdate = st.date_input("日付", key="mdate")
        tournament = st.text_input("大会名")
        opponent = st.text_input("対戦相手")
        waza = st.text_input("決めた技（例：背負い投げ）")
        result_type = st.selectbox("決まり手", ["一本", "技あり", "判定"])
        time_sec = st.number_input("試合時間（秒）", min_value=0)
        hansoku = st.selectbox("反則", ["なし", "指導", "反則負け"])
        msubmit = st.form_submit_button("追加")

    if msubmit:
        new_data = pd.DataFrame([[mdate, tournament, opponent, waza, result_type, time_sec, hansoku]],
                                columns=match_df.columns)
        match_df = pd.concat([match_df, new_data], ignore_index=True)
        match_df.to_csv(MATCH_CSV, index=False)
        st.success("保存しました！")

    st.subheader("📌 試合履歴")
    st.dataframe(match_df, use_container_width=True)

    if not match_df.empty:
        st.subheader("🥋 決め技ランキング")
        st.bar_chart(match_df["技"].value_counts())


# ============ パフォーマンス統計 ============
with tab3:
    st.header("📊 練習 × 試合の関係分析")

    if practice_df.empty or match_df.empty:
        st.warning("練習データと試合データの両方が必要です！")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("練習時間と勝率の傾向")
            merged = practice_df.copy()
            st.scatter_chart(merged, x="練習時間(分)", y="勝率")

        with col2:
            st.subheader("コンディションと勝率の関係")
            st.scatter_chart(practice_df, x="コンディション", y="勝率")


# ============ データ確認 =============
with tab4:
    st.header("📁 保存ファイル")
    st.write("📌 練習データ → practice.csv")
    st.write("📌 試合データ → match.csv")
    st.download_button("練習CSVをダウンロード", data=practice_df.to_csv(index=False), file_name="practice.csv")
    st.download_button("試合CSVをダウンロード", data=match_df.to_csv(index=False), file_name="match.csv")

