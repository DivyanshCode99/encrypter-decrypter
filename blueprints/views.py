from flask import Blueprint ,render_template, send_file
import os

views=Blueprint("views",__name__)


@views.route("/")
def home():
    return render_template("home.html")


if __name__ =="__main__":
    print("Please run the main.py file.")