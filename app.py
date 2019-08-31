import random

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for


df = pd.read_csv("qs.csv", header=None, index_col=None)
count = 1
correct_count = 0

flag = True
ans1 = ans2 = None

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
    global count, df, flag, ans1, ans2, correct_count
    print(flag, "flag")
    if flag:
        ans1 = random.randint(0, 1)
        print(df.iloc[count - 1, ans1 + 1], ans1)
        ans2 = 1 - ans1
        flag = False
    if len(df) == count:
        return redirect(url_for("result"))
    else:
        if request.method == "GET":
            return render_template("index.html", number=count, ans1=df.iloc[count - 1, ans1 + 1],
                                   ans2=df.iloc[count - 1, ans2 + 1], question=df.iloc[count - 1, 0])
        else:
            memo = int(request.form["1"])
            count += 1
            # print(ans1, memo)
            ex = df.iloc[count - 2, 3]
            cr = df.iloc[count - 2, 1]
            flag = True
            if (ans1 == 0 and memo == 0) | (ans1 == 1 and memo == 1):
                correct_count += 1
                print("correct answer")
                return redirect(url_for("correct", ans11=cr, ans22=cr,
                                        explain=ex, number=count - 1))

            else:
                print("wrong answer")
                return redirect(url_for("wrong", ans11=cr, ans22=df.iloc[count - 2, 2],
                                        explain=ex, number=count - 1))


@app.route("/correct/<string:ans11>/<string:ans22>/<string:explain>/<int:number>", methods=["GET", "POST"])
def correct(ans11, ans22, explain, number):
    # print(request.form["next"])
    if request.method == "GET":
        return render_template("correct.html", number=number, ans1=ans11, ans2=ans22, explain=explain)
    else:
        return redirect(url_for("quiz"))


@app.route("/wrong/<string:ans11>/<string:ans22>/<string:explain>/<int:number>", methods=["GET", "POST"])
def wrong(number, ans11, ans22, explain):
    # print(request.form["start"])
    if request.method == "GET":
        return render_template("wrong.html", number=number, ans1=ans11, ans2=ans22, explain=explain)
    else:
        return redirect(url_for("quiz"))


@app.route("/result", methods=["GET", "POST"])
def result():
    global count, correct_count
    pie_plot(correct_count, count - 1 - correct_count)
    print(request.method)
    if request.method == "GET":
        return render_template("result.html", count=count - 1, correct_count=correct_count)
    else:
        correct_count = 0
        count = 1
        return redirect(url_for("title"))


def pie_plot(co, wr):
    labels = ["Correct", "Wrong"]
    x = [co, wr]
    plt.pie(x, labels=labels, counterclock=False, startangle=90, autopct="%1.1f%%")
    plt.legend(labels, fontsize=12)
    plt.savefig("static/images/pie_plot.png")
    plt.cla()


if __name__ == '__main__':
    app.run(debug=True)
