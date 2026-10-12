# app.py — главный файл сервера
from flask import Flask, render_template, request, session, redirect, url_for
import random
from questions import ALGEBRA, GEOMETRY

app = Flask(__name__)
app.secret_key = "ege_secret_key_2024"  # нужен для сессий

def normalize(s: str) -> str:
    """Убирает пробелы и приводит к нижнему регистру."""
    return s.replace(" ", "").replace("²", "^2").replace("³", "^3").lower()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train/<topic>", methods=["GET", "POST"])
def train(topic):
    if topic not in ("algebra", "geometry"):
        return redirect(url_for("index"))

    bank = ALGEBRA if topic == "algebra" else GEOMETRY

    # Новая карточка
    if request.method == "POST" and "next" in request.form:
        session.pop("current_q", None)
        session.pop("feedback", None)
        return redirect(url_for("train", topic=topic))

    # Инициализация вопроса
    if "current_q" not in session or session.get("topic") != topic:
        session["current_q"] = random.randint(0, len(bank) - 1)
        session["topic"] = topic
        session["score"] = session.get("score", 0)
        session["total"] = session.get("total", 0)

    idx = session["current_q"]
    item = bank[idx]
    feedback = None

    # Проверка ответа
    if request.method == "POST" and "answer" in request.form:
        user_ans = normalize(request.form["answer"])
        correct = normalize(item["a"])
        session["total"] = session.get("total", 0) + 1
        if user_ans == correct:
            session["score"] = session.get("score", 0) + 1
            feedback = ("ok", "✅ Верно!")
        else:
            feedback = ("bad", f"❌ Неверно. Правильный ответ: {item['a']}")

    return render_template(
        "train.html",
        topic=topic,
        question=item["q"],
        hint=item["hint"],
        feedback=feedback,
        score=session.get("score", 0),
        total=session.get("total", 0),
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)