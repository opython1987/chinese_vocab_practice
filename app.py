# app.py — メニューに3ボタン＋各ページに遷移（Streamlit 1.50）
import random
import streamlit as st

st.set_page_config(page_title="中国語学習アプリ", page_icon="📘", layout="centered")

# ===== ルータ状態 =====
if "page" not in st.session_state:
    st.session_state.page = "menu"  # menu / vocab / tone / tts

def go_menu():  st.session_state.page = "menu"
def go_vocab(): st.session_state.page = "vocab"
def go_tone():  st.session_state.page = "tone"
def go_tts():   st.session_state.page  = "tts"

# ===== 単語データ =====
word_list = [
    {"japanese": "こんにちは", "chinese": "你好"},
    {"japanese": "ありがとう", "chinese": "謝謝"},
    {"japanese": "さようなら", "chinese": "再見"},
    {"japanese": "水", "chinese": "水"},
    {"japanese": "ご飯", "chinese": "米飯"},
]

# ==== 四声テスト用データ ====
tone_words = [
    {"chinese": "台湾",   "pinyin": "tái wān",     "tones": [2, 1]},
    {"chinese": "謝謝",   "pinyin": "xiè xie",     "tones": [4, 5]},  # 軽声は5
    {"chinese": "再見",   "pinyin": "zài jiàn",    "tones": [4, 4]},
    {"chinese": "水",     "pinyin": "shuǐ",        "tones": [3]},
    {"chinese": "米飯",   "pinyin": "mǐ fàn",      "tones": [3, 4]},
    {"chinese": "朋友",   "pinyin": "péng yǒu",    "tones": [2, 3]},
    {"chinese": "老師",   "pinyin": "lǎo shī",     "tones": [3, 1]},
]


# ===== メニュー画面 =====
def show_menu():
    st.markdown("<h1 style='text-align:center'>🇹🇼 中国語学習アプリ</h1>", unsafe_allow_html=True)
    st.subheader("メニュー")
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("📘 単語テスト（漢字）", use_container_width=True, on_click=go_vocab)
    with c2:
        st.button("4️⃣ 四声テスト", use_container_width=True, on_click=go_tone)
    with c3:
        st.button("🔊 音声読み上げ", use_container_width=True, on_click=go_tts)
    st.write("---")
    st.caption("ボタンでページを切り替える方式（サイドバーは使いません）")

# ===== 単語テスト（漢字） =====
def show_vocab():
    st.header("📘 中国語（繁体字）単語練習アプリ")
    st.button("⬅ メニューに戻る", on_click=go_menu)

    # 状態（vocab_ で名前空間）
    if "vocab_questions" not in st.session_state:
        st.session_state.vocab_questions = random.sample(word_list, len(word_list))
    if "vocab_score" not in st.session_state:
        st.session_state.vocab_score = 0
    if "vocab_current" not in st.session_state:
        st.session_state.vocab_current = 0
    if "vocab_result" not in st.session_state:
        st.session_state.vocab_result = None

    def reset_quiz():
        st.session_state.vocab_questions = random.sample(word_list, len(word_list))
        st.session_state.vocab_score = 0
        st.session_state.vocab_current = 0
        st.session_state.vocab_result = None
        st.rerun()

    if st.session_state.vocab_current >= len(st.session_state.vocab_questions):
        st.success(f"終了！スコア: {st.session_state.vocab_score} / {len(st.session_state.vocab_questions)}")
        st.button("もう一度", on_click=reset_quiz)
    else:
        q = st.session_state.vocab_questions[st.session_state.vocab_current]
        st.markdown(f"**日本語:**  **{q['japanese']}**")
        with st.form(key=f"vocab_form_{st.session_state.vocab_current}", clear_on_submit=False):
            input_key = f"vocab_answer_{st.session_state.vocab_current}"
            answer = st.text_input("中国語（繁体字）で入力", key=input_key)
            submitted = st.form_submit_button("送信")
        if submitted:
            correct = q["chinese"]
            if answer.strip() == correct:
                st.session_state.vocab_result = "✅ 正解！"
                st.session_state.vocab_score += 1
            else:
                st.session_state.vocab_result = f"❌ 不正解。正しい答えは：{correct}"
            st.session_state.vocab_current += 1
            st.rerun()
        if st.session_state.vocab_result:
            st.info(st.session_state.vocab_result)
        st.caption(f"スコア: {st.session_state.vocab_score} / {st.session_state.vocab_current}")

    st.divider()
    st.button("リセット（最初から）", on_click=reset_quiz)

# ===== 四声テスト（プレースホルダ） =====
def show_tone():
    import random
    st.header("4️⃣ 四声テスト（数字で入力）")
    st.button("⬅ メニューに戻る", on_click=go_menu)

    # ---- 初期化 ----
    if "tone_questions" not in st.session_state:
        st.session_state.tone_questions = random.sample(tone_words, len(tone_words))
        st.session_state.tone_current = 0
        st.session_state.tone_score = 0
        st.session_state.tone_result = None

    qs = st.session_state.tone_questions
    i  = st.session_state.tone_current

    # ---- 終了判定 ----
    if i >= len(qs):
        st.success(f"終了！スコア: {st.session_state.tone_score} / {len(qs)}")
        if st.button("もう一度"):
            for k in ["tone_questions","tone_current","tone_score","tone_result"]:
                st.session_state.pop(k, None)
            st.rerun()
        return

    # ---- 出題 ----
    q = qs[i]  # {"chinese":..., "pinyin":..., "tones":[...]}
    syllables = len(q["tones"])
    st.markdown(f"**漢字**：**{q['chinese']}**")
    st.caption(f"各音節の声調を**数字**で連続入力してください（例：台湾 → 2と1 なので **21**）。\n"
               f"音節数：{syllables} / 入力可能: 1,2,3,4,5（5=軽声）")

    # 入力フォーム（数字のみ）
    with st.form(key=f"tone_form_{i}", clear_on_submit=False):
        ans = st.text_input("声調番号（例：21 / 44 / 3 など）", key=f"tone_ans_{i}")
        submitted = st.form_submit_button("判定")

    if submitted:
        # 前処理：全角→半角、空白・記号削除
        import re
        normalized = re.sub(r"\D", "", ans)  # 数字以外除去
        expected = "".join(str(t) for t in q["tones"])
        # まず桁数チェック
        if len(normalized) != len(expected):
            st.session_state.tone_result = f"⚠ 入力桁数が違います（必要: {len(expected)} 桁）。例：{expected}"
        else:
            if normalized == expected:
                st.session_state.tone_result = f"✅ 正解！ → {q['pinyin']}（{expected}）"
                st.session_state.tone_score += 1
            else:
                st.session_state.tone_result = f"❌ 不正解… 正解は {expected}（{q['pinyin']}）"
            # 次の問題へ
            st.session_state.tone_current += 1
            st.rerun()

    # 直前の結果
    if st.session_state.tone_result:
        st.info(st.session_state.tone_result)

    st.caption(f"スコア: {st.session_state.tone_score} / {st.session_state.tone_current}")


# ===== 音声読み上げ（プレースホルダ） =====

def show_tts():
    import os, httpx, re
    import streamlit as st

    st.header("🔊 中国語（繁體）音声読み上げ（診断モード）")
    st.button("⬅ メニューに戻る", on_click=go_menu)

    SPEECH_KEY = os.getenv("SPEECH_KEY")
    SPEECH_REGION = os.getenv("SPEECH_REGION")

    txt = st.text_area("中国語テキスト（繁/簡）", "大家好，歡迎來到這個中文學習小工具。", height=120)

    col1, col2, col3 = st.columns(3)
    with col1:
        voice = st.selectbox("ボイス", [
            "zh-TW-HsiaoChenNeural",
            "zh-TW-HsiaoYuNeural",
            "zh-TW-YunJheNeural",
        ])
    with col2:
        rate  = st.text_input("速度", "0%", help="例: +10% / -10% / 0%")
    with col3:
        pitch = st.text_input("ピッチ", "0%", help="例: +2st / -2st / 0%")

    st.markdown("**出力フォーマット（まず MP3 48kHz → ダメなら WAV を試す）**")
    fmt = st.radio(
        "フォーマット",
        ["MP3 (48kHz)", "WAV (48kHz)"],
        index=0,
        help="iOSは48kHzが安定。MP3で無音ならWAVを試してください。"
    )

    if st.button("▶ 合成して再生", type="primary"):
        if not (SPEECH_KEY and SPEECH_REGION):
            st.error("SPEECH_KEY / SPEECH_REGION が未設定です（Secrets または環境変数を設定）")
            return

        # Azure エンドポイント
        token_url = f"https://{SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        tts_url   = f"https://{SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

        # 出力フォーマット設定（iOS互換を優先）
        if fmt == "MP3 (48kHz)":
            output_format = "audio-48khz-96kbitrate-mono-mp3"
            mime = "audio/mpeg"   # ← iOS/Android/PCで互換性高い
            audio_arg = "audio/mpeg"
        else:
            output_format = "riff-48khz-16bit-mono-pcm"
            mime = "audio/wav"
            audio_arg = "audio/wav"

        try:
            with httpx.Client(timeout=30) as client:
                # 1) トークン取得
                r = client.post(token_url, headers={"Ocp-Apim-Subscription-Key": SPEECH_KEY})
                r.raise_for_status()
                token = r.text

                # 2) SSML
                # 安全のため、不正な制御文字を除去
                safe_txt = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", txt)
                ssml = f"""
<speak version="1.0" xml:lang="zh-TW">
  <voice name="{voice}">
    <prosody rate="{rate}" pitch="{pitch}">{safe_txt}</prosody>
  </voice>
</speak>
""".strip()

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/ssml+xml",
                    "X-Microsoft-OutputFormat": output_format,
                    "User-Agent": "streamlit-zh-tw-tts",
                }

                # 3) 合成
                t = client.post(tts_url, headers=headers, content=ssml.encode("utf-8"))
                t.raise_for_status()
                audio_bytes = t.content

            # ===== 診断表示 =====
            st.markdown("### 🔍 Diagnostics")
            st.write(f"- Bytes length: **{len(audio_bytes)}**")
            st.write(f"- First 16 bytes (hex): `{audio_bytes[:16].hex()}`")
            st.write(f"- OutputFormat: `{output_format}` / MIME: `{mime}`")

            if len(audio_bytes) == 0:
                st.error("合成結果が空です。キー/リージョン/テキストを確認してください。")
                return

            # ===== 再生と保存（MP3/WAV） =====
            st.markdown("### ▶ 再生")
            st.audio(audio_bytes, format=audio_arg)

            st.download_button(
                "音声を保存",
                data=audio_bytes,
                file_name="tts.mp3" if mime == "audio/mpeg" else "tts.wav",
                mime=mime,
                use_container_width=True,
            )

            # iOS向けヒント
            if fmt == "MP3 (48kHz)":
                st.caption("※ iPhoneで無音なら、上のフォーマットを **WAV (48kHz)** に切り替えて再試行してください。")
            else:
                st.caption("※ WAVでも再生できない場合は端末のサイレントスイッチ/音量も確認してください。")

        except Exception as e:
            st.error(f"読み上げに失敗：{e}")


# ===== 画面分岐 =====
page = st.session_state.page
if page == "menu":
    show_menu()
elif page == "vocab":
    show_vocab()
elif page == "tone":
    show_tone()
elif page == "tts":
    show_tts()
