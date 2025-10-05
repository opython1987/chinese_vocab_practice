# app.py ー Streamlit版：中国語（繁体字）単語練習アプリ
import random
import streamlit as st

# ---- データ ----
word_list = [
    {"japanese": "こんにちは", "chinese": "你好"},
    {"japanese": "ありがとう", "chinese": "謝謝"},
    {"japanese": "さようなら", "chinese": "再見"},
    {"japanese": "水", "chinese": "水"},
    {"japanese": "ご飯", "chinese": "米飯"},
]

# ---- 初期化 ----
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(word_list, len(word_list))
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = 0
if "result" not in st.session_state:
    st.session_state.result = None

def reset_quiz():
    st.session_state.questions = random.sample(word_list, len(word_list))
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.result = None
    st.rerun()

st.set_page_config(page_title="中国語（繁体字）単語練習アプリ", page_icon="📘", layout="centered")
st.title("中国語（繁体字）単語練習アプリ")

# ---- 終了判定 ----
if st.session_state.current >= len(st.session_state.questions):
    st.success(f"終了！あなたのスコア: {st.session_state.score} / {len(st.session_state.questions)}")
    st.button("もう一度", on_click=reset_quiz)
else:
    q = st.session_state.questions[st.session_state.current]
    st.markdown(f"**日本語:**  **{q['japanese']}**")

    # 入力フォーム（1回の送信で評価）
    with st.form(key="answer_form", clear_on_submit=False):
        input_key = f"answer_{st.session_state.current}"
        answer = st.text_input("中国語（繁体字）で入力", key=input_key)
        submitted = st.form_submit_button("送信")

    # 判定処理
    if submitted:
        correct = q["chinese"]
        # そのまま完全一致判定（必要なら大小/空白の調整はここで）
        if answer.strip() == correct:
            st.session_state.result = "✅ 正解！"
            st.session_state.score += 1
        else:
            st.session_state.result = f"❌ 不正解。正しい答えは：{correct}"
        st.session_state.current += 1
        # 次の問題に進むため、入力欄をクリア
        st.rerun()

    # 直前の判定結果を表示
    if st.session_state.result:
        st.info(st.session_state.result)

    st.caption(f"スコア: {st.session_state.score} / {st.session_state.current}")

# 下部にリセットボタン（いつでも使える）
st.divider()
st.button("リセット（最初から）", on_click=reset_quiz)


