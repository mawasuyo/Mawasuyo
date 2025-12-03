import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="柔道トレーニング記録", layout="wide")

st.title("🥋 柔道トレーニング記録アプリ")

# CSV 読み込み（存在しない場合は新規 DataFrame）
def load_history():
    try:
        return pd.read_csv("training_history.csv")
    except:
        return pd.DataFrame(columns=[
            "日付", "練習内容", "立ち技", "寝技", "練習時間(分)", "コンディション"
        ])

def save_history(df):
    df.to_csv("training_history.csv", index=False)

history = load_history()

# -----------------------------
# 入力フォーム
# -----------------------------
st.header("📘 今日の練習内容を記録")

with st.form("training_form"):
    date = st.date_input("日付", datetime.now())

    st.subheader("🔽 練習内容（複数選択OK）")
    practice_items = st.multiselect(
        "練習内容",
        [
            "打ち込み",
            "スピード打ち込み",
            "三人打ち込み",
            "移動打ち込み",
            "一本取り",
            "乱取り",
            "寝技",
            "投げ込み",
            "補強トレーニング",
            "フリー練習",
        ]
    )

    st.subheader("🔽 立ち技（投げた技）")
    standing_techniques = st.multiselect(
        "立ち技",
        [
            "大外刈",
            "大内刈",
            "内股",
            "背負い投げ",
            "小外刈",
            "浮落",
            "巴投げ",
            "支えつり込み足",
            "体落とし",
            "払い腰",
        ]
    )

    st.subheader("🔽 寝技（カテゴリ）")
    ground_categories = st.multiselect(
        "寝技カテゴリ",
        ["抑え込み", "締め技", "関節技"]
    )

    time_min = st.number_input("練習時間（分）", min_value=0, value=60)
    condition = st.slider("コンディション（1〜10）", 1, 10, 7)

    submitted = st.form_submit_button("記録する")

# 記録処理
if submitted:
    new_record = pd.DataFrame([{
        "日付": date.strftime("%Y-%m-%d"),
        "練習内容": " / ".join(practice_items),
        "立ち技": " / ".join(standing_techniques),
        "寝技": " / ".join(ground_categories),
        "練習時間(分)": time_min,
        "コンディション": condition
    }])

    history = pd.concat([history, new_record], ignore_index=True)
    save_history(history)
    st.success("記録を保存しました！")

# -----------------------------
# 履歴表示
# -----------------------------
st.header("📚 トレーニング履歴")
st.dataframe(history, use_container_width=True)

# -----------------------------
# グラフ表示
# -----------------------------
st.header("📈 練習時間・コンディション 推移グラフ")

if len(history) > 0:
    history_plot = history.copy()
    history_plot["日付"] = pd.to_datetime(history_plot["日付"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏱ 練習時間の推移")
        st.line_chart(history_plot.set_index("日付")["練習時間(分)"])

    with col2:
        st.subheader("💡 コンディションの推移")
        st.line_chart(history_plot.set_index("日付")["コンディション"])

else:
    st.info("まだ記録がありません。まずは練習を記録してみましょう。")

st.write("---")
st.caption("© 2025 柔道トレーニング記録アプリ")

