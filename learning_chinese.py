from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッション管理用の秘密鍵

word_list = [
    {"japanese": "こんにちは", "chinese": "你好"},
    {"japanese": "ありがとう", "chinese": "謝謝"},
    {"japanese": "さようなら", "chinese": "再見"},
    {"japanese": "水", "chinese": "水"},
    {"japanese": "ご飯", "chinese": "米飯"},
]

TEMPLATE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>中国語（繁体字）単語練習アプリ</title>
</head>
<body>
    <h2>中国語（繁体字）単語練習アプリ</h2>
    {% if finished %}
        <p>終了！あなたのスコア: {{score}} / {{total}}</p>
        <a href="{{ url_for('start') }}">もう一度</a>
    {% else %}
        <p>日本語: <b>{{japanese}}</b></p>
        <form method="post">
            <input name="answer" autocomplete="off" autofocus>
            <input type="submit" value="送信">
        </form>
        {% if result is not none %}
            <p>{{ result }}</p>
        {% endif %}
        <p>スコア: {{score}} / {{current}}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def start():
    session["questions"] = random.sample(word_list, len(word_list))
    session["score"] = 0
    session["current"] = 0
    session["result"] = None
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = session.get("questions", [])
    score = session.get("score", 0)
    current = session.get("current", 0)
    result = session.get("result", None)

    if current >= len(questions):
        return render_template_string(TEMPLATE, finished=True, score=score, total=len(questions))

    if request.method == "POST":
        answer = request.form.get("answer", "").strip()
        correct = questions[current]["chinese"]
        if answer == correct:
            result = "正解！"
            score += 1
        else:
            result = f"不正解。正しい答えは: {correct}"
        current += 1
        session["score"] = score
        session["current"] = current
        session["result"] = result
        return redirect(url_for("quiz"))

    japanese = questions[current]["japanese"]
    return render_template_string(
        TEMPLATE,
        finished=False,
        japanese=japanese,
        score=score,
        current=current,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)

