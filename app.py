from flask import Flask, make_response, render_template, request, redirect, url_for
import pandas as pd
import random

df = pd.read_csv("questions.csv", header=None, index_col=None)
print(df)
count = 1

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def title():
    action = request.form.getlist("action")
    if request.method == "GET":
        return render_template("title.html")
    else:
        return redirect(url_for)


@app.route("/question", methods=["GET", "POST"])
def quiz():
    global count, df
    ans1 = random.randint(0, 1)
    ans2 = 1 - ans1
    print(df.iloc[ans1, count - 1])
    if request.method == "GET":
        # print(count)
        return render_template("index.html", number=count, ans1=df.iloc[count - 1, ans1 + 1],
                               ans2=df.iloc[count - 1, ans2 + 1], question=df.iloc[count - 1, 0])
    elif request.form["ans"]:
        memo = request.form["ans"]
        count += 1
        print(memo, "a")
        if memo == str(ans1):
            print("correct answer")
            return redirect(url_for("/correct"))
        else:
            return redirect(url_for("/wrong"))
    else:
        return render_template("index.html")


@app.route("/correct", methods=["GET", "POST"])
def correct():
    print("aa")
    if request.method == "GET":
        return render_template("correct.html")
    else:
        return redirect(url_for("/question"))


@app.route("/wrong")
def wrong():
    print("bb")
    if request.method == "GET":
        return render_template("wrong.html")
    else:
        return redirect(url_for("/question"))


if __name__ == '__main__':
    app.run(debug=True)
