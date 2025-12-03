import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.title("柔道 練習記録アプリ🥋")
menu = st.sidebar.selectbox("メニューを選択", ["練習記録を入力", "記録を見る", "グラフで見る"])

CSV_FILE = "training_data.csv"

# ------ CSVがなければ作成 ------
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "日付", "練習内容", "練習時間(分)", "コンディション", "投げた技"
    ])
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

# ------ 練習記録ページ ------
if menu == "練習記録を入力":
    st.header("📌 練習内容を記録")
    
    date = st.date_input("日付")
    
    # 練習内容チェックボックス
    practice_options = [
        "打ち込み", "スピード打ち込み", "三人打ち込み", "移動打ち込み",
        "一本取り", "乱取り", "寝技", "投げ込み", "補強トレーニング", "フリー練習"
    ]
    practice_selected = st.multiselect("練習内容を選択", practice_options)
    
    minutes = st.number_input("練習時間（分）", min_value=0)
    condition = st.number_input("コンディション（1〜10）", min_value=1, max_value=10)
    
    # 投げた技チェックボックス
    standing_techniques = [
        "大外刈", "大内刈", "内股", "背負い投げ", "小外刈", "巴投げ",
        "支えつり込み足", "体落とし", "払い腰", "肩車"
    ]
    ground_techniques = ["抑え込み", "締め技", "関節技"]
    techniques_selected = st.multiselect("立ち技を選択", standing_techniques)
    techniques_selected += st.multiselect("寝技を選択", ground_techniques)
    
    if st.button("保存"):
        new = pd.DataFrame([[
            date, ", ".join(practice_selected), minutes, condition, ", ".join(techniques_selected)
        ]], columns=["日付", "練習内容", "練習時間(分)", "コンディション", "投げた技"])
        
        old = pd.read_csv(CSV_FILE)
        updated = pd.concat([old, new], ignore_index=True)
        updated.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        st.success("保存しました！💾")

# ------ 記録一覧ページ ------
elif menu == "記録を見る":
    st.header("📋 練習記録一覧")
    df = pd.read_csv(CSV_FILE)
    
    if len(df) == 0:
        st.info("まだ記録がありません。")
    else:
        st.dataframe(df)

# ------ グラフページ ------
elif menu == "グラフで見る":
    st.header("📈 練習時間とコンディションの推移")
    df = pd.read_csv(CSV_FILE)
    
    if len(df) == 0:
        st.info("グラフを表示するには記録を追加してください。")
    else:
        df["日付"] = pd.to_datetime(df["日付"])
        df = df.sort_values("日付")
        
        # 練習時間グラフ
        st.subheader("練習時間の推移")
        plt.figure()
        plt.plot(df["日付"], df["練習時間(分)"], marker="o")
        plt.xlabel("日付")
        plt.ylabel("練習時間(分)")
        plt.title("練習時間の変化")
        st.pyplot(plt)
        
        # コンディショングラフ
        st.subheader("コンディションの波")
        plt.figure()
        plt.plot(df["日付"], df["コンディション"], marker="o", color="orange")
        plt.xlabel("日付")
        plt.ylabel("コンディション(1〜10)")
        plt.title("コンディションの変化")
        st.pyplot(plt)


