from flask import Flask, redirect, url_for, render_template, request
import twitter2
app = Flask(__name__)


@app.route("/map")
def get_map():
    return render_template('my_map3.html')


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        if twitter2.search(user):
            return redirect(url_for("get_map"))
    else:
        return render_template("run.html")


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)

