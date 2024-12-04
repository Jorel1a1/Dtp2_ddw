from app import application
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from urllib.parse import urlparse, unquote
from app import db
from flask import request
from app.serverlibrary import mergesort  # , #EvaluateExpression, get_smallest_three
import numpy as np


@application.route("/")
@application.route("/index/")
@login_required
def index():
    prefix = application.wsgi_app.prefix[:-1]
    return render_template("index.html", title="Home", prefix=prefix)


@application.route("/users/")
@login_required
def users():
    prefix = application.wsgi_app.prefix[:-1]
    users = User.query.all()
    mergesort(users, lambda item: item.username)
    usernames = [u.username for u in users]
    return render_template("users.html", title="Users", users=usernames, prefix=prefix)


@application.route("/login/", methods=["GET", "POST"])
def login():
    prefix = application.wsgi_app.prefix[:-1]
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = unquote(request.args.get("next", url_for("index")))
        if next_page:
            next_page = unquote(next_page)  # Decode the next page

        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form, prefix=prefix)


@application.route("/logout/")
def logout():
    prefix = application.wsgi_app.prefix[:-1]
    logout_user()
    return redirect(url_for("index"))


@application.route("/register/", methods=["GET", "POST"])
def register():
    prefix = application.wsgi_app.prefix[:-1]
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user.")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form, prefix=prefix)


@application.route("/predict_us/", methods=["POST"])
def US():
    f = open("Betavalues.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "us":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            betaVal = np.array([val])
    f.close()
    f = open("FQ.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "us":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    fq = (float(request.form["FQ"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("ML.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "us":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ml = (float(request.form["ML"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("AA.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "us":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    aa = (float(request.form["AA"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("IA.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "us":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ia = (float(request.form["IA"]) - minMax[0]) / (minMax[1] - minMax[0])
    x = np.array([1, fq, ml, aa, ia])
    predictedVal = x @ betaVal.T
    predictedVal = predictedVal.flatten()
    return render_template("predict.html", prediction_text=f"Predicted Value: {predictedVal}")


@application.route("/predict_aus/", methods=["POST"])
def AUS():
    f = open("Betavalues.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "aus":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            betaVal = np.array([val])
    f.close()
    f = open("FQ.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "aus":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    fq = (float(request.form["FQ"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("ML.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "aus":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ml = (float(request.form["ML"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("II.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "aus":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ii = (float(request.form["II"]) - minMax[0]) / (minMax[1] - minMax[0])
    x = np.array([1, fq, ml, ii])
    predictedVal = x @ betaVal.T
    predictedVal = predictedVal.flatten()
    return render_template("predict.html", prediction_text=f"Predicted Value: {predictedVal}")


@application.route("/predict_can/", methods=["POST"])
def CAN():
    f = open("Betavalues.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "can":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            betaVal = np.array([val])
    f.close()
    f = open("FQ.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "can":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    fq = (float(request.form["FQ"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("ML.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "can":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ml = (float(request.form["ML"]) - minMax[0]) / (minMax[1] - minMax[0])
    x = np.array([1, fq, ml])
    predictedVal = x @ betaVal.T
    predictedVal = predictedVal.flatten()
    return render_template("predict.html", prediction_text=f"Predicted Value: {predictedVal}")


@application.route("/predict_china/", methods=["POST"])
def CHINA():
    f = open("Betavalues.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "china":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            betaVal = np.array([val])
    f.close()
    f = open("ML.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "china":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ml = (float(request.form["ML"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("AA.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "china":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    aa = (float(request.form["AA"]) - minMax[0]) / (minMax[1] - minMax[0])
    x = np.array([1, ml, aa])
    predictedVal = x @ betaVal.T
    predictedVal = predictedVal.flatten()
    return render_template("predict.html", prediction_text=f"Predicted Value: {predictedVal}")


@application.route("/predict_india/", methods=["POST"])
def INDIA():
    f = open("Betavalues.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "india":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            betaVal = np.array([val])
    f.close()
    f = open("ML.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "india":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    ml = (float(request.form["ML"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("AL.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "india":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    al = (float(request.form["AL"]) - minMax[0]) / (minMax[1] - minMax[0])
    x = np.array([1, ml, al])
    predictedVal = x @ betaVal.T
    predictedVal = predictedVal.flatten()
    return render_template("predict.html", prediction_text=f"Predicted Value: {predictedVal}")


@application.route("/predict_mexico/", methods=["POST"])
def MEXICO():
    f = open("Betavalues.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "mexico":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            betaVal = np.array([val])
    f.close()
    f = open("FQ.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "mexico":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    fq = (float(request.form["FQ"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("AA.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "mexico":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    aa = (float(request.form["AA"]) - minMax[0]) / (minMax[1] - minMax[0])
    f = open("AL.txt", "r")
    lines = f.readlines()
    for line in lines:
        array = line.split()
        if array[0] == "mexico":
            val = []
            for i in range(1, len(array)):
                val.append(float(array[i]))
            minMax = val
    f.close()
    al = (float(request.form["AL"]) - minMax[0]) / (minMax[1] - minMax[0])
    x = np.array([1, fq, aa, al])
    predictedVal = x @ betaVal.T
    predictedVal = predictedVal.flatten()
    return render_template("predict.html", prediction_text=f"Predicted Value: {predictedVal}")


@application.route("/predict/")
@login_required
def predict():
    return render_template("predict.html")
