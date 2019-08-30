from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random

df = pd.read_csv("qs.csv", header=None, index_col=None)
count = 1

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def title():
    if request.method == "GET":
        return render_template("title.html")
    else:
        return redirect(url_for("quiz"))


@app.route("/question", methods=["GET", "POST"])
def quiz():
    # データ呼び出し
    global count, df
    ans1 = random.randint(0, 1)
    print(df.iloc[count - 1, ans1 + 1], ans1)
    ans2 = 1 - ans1
    if len(df) == count:
        return redirect(url_for("result"))
    else:
        if request.method == "GET":
            return render_template("index.html", number=count, ans1=df.iloc[count - 1, ans1 + 1],
                                   ans2=df.iloc[count - 1, ans2 + 1], question=df.iloc[count - 1, 0])
        else:
            memo = int(request.form["1"])
            count += 1
            print(ans1, memo)
            ex = df.iloc[count - 2, 3]
            cr = df.iloc[count - 2, 1]
            if (ans1 == 0 and memo == 0) | (ans1 == 1 and memo == 1):
                print("correct answer")
                return redirect(url_for("correct", ans1=cr, ans2=cr,
                                        explain=ex, number=count - 1))

            else:
                print("wrong answer")
                return redirect(url_for("wrong", ans1=cr, ans2=df.iloc[count - 2, 2],
                                        explain=ex, number=count - 1))


@app.route("/correct/<string:ans1>/<string:ans2>/<string:explain>/<int:number>", methods=["GET", "POST"])
def correct(number, ans1, ans2, explain):
    if request.method == "GET":
        return render_template("correct.html", number=number, ans1=ans1, ans2=ans2, explain=explain)
    else:
        return redirect(url_for("question"))

@app.route("/wrong/<string:ans1>/<string:ans2>/<string:explain>/<int:number>", methods=["GET", "POST"])
def wrong(number, ans1, ans2, explain):
    if request.method == "GET":
        return render_template("wrong.html", number=number, ans1=ans1, ans2=ans2, explain=explain)
    else:
        return redirect(url_for("question"))


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "GET":
        return "hello"
    else:
        return "result"


if __name__ == '__main__':
    app.run(debug=True)
