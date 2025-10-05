# app.py — Streamlit 1.50対応・ボタンでページ遷移するメニュー方式
import streamlit as st

st.set_page_config(page_title="中国語学習メニュー", page_icon="📘")

# ページ状態を初期化
if "page" not in st.session_state:
    st.session_state.page = "menu"

# ページ切り替え関数
def go_menu():
    st.session_state.page = "menu"

def go_vocab():
    st.session_state.page = "vocab"

def go_tone():
    st.session_state.page = "tone"

def go_tts():
    st.session_state.page = "tts"

# =====================
# ページ1：メニュー画面
# =====================
def show_menu():
    st.markdown("<h1 style='text-align:center;'>🇹🇼 中国語学習アプリ</h1>", unsafe_allow_html=True)
    st.subheader("メニュー")
    st.write("---")

    # ボタンを横並びで配置
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📘 単語テスト（漢字）", use_container_width=True, on_click=go_vocab)
    with col2:
        st.button("4️⃣ 四声テスト", use_container_width=True, on_click=go_tone)
    with col3:
        st.button("🔊 音声読み上げ", use_container_width=True, on_click=go_tts)

    st.write("---")
    st.caption("ボタンでページを切り替える方式（サイドバーは使いません）")

# =====================
# ページ2：単語テスト
# =====================
def show_vocab():
    st.header("📘 単語テスト（漢字）")
    st.write("ここに単語テストの機能を追加します。")
    st.button("⬅ メニューに戻る", on_click=go_menu)

# =====================
# ページ3：四声テスト
# =====================
def show_tone():
    st.header("4️⃣ 四声テスト")
    st.write("ここに四声テストの機能を追加します。")
    st.button("⬅ メニューに戻る", on_click=go_menu)

# =====================
# ページ4：音声読み上げ
# =====================
def show_tts():
    st.header("🔊 音声読み上げ")
    st.write("ここにAzure TTSなどを追加します。")
    st.button("⬅ メニューに戻る", on_click=go_menu)

# =====================
# ページ遷移の制御
# =====================
if st.session_state.page == "menu":
    show_menu()
elif st.session_state.page == "vocab":
    show_vocab()
elif st.session_state.page == "tone":
    show_tone()
elif st.session_state.page == "tts":
    show_tts()
