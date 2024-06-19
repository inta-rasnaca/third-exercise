"""
Simple Flask application that runs chat-like message service with sqlite database
"""

from flask import (
    Flask,
    request,
    render_template,
    flash,
    redirect
)
from sqlite3 import connect
from uuid import uuid4

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# Example 1
""" @app.route("/")
def index():
    return "Hello World" """

# Example 2
""" @app.route("/")
def index():
    return render_template("hello_world.html", my_text="😊 This is my Flask page 😊") """

@app.route("/")
def main_page():
    return render_template("main_panel.html")

# Example 3
@app.route("/send", methods=["POST"])
def send_message():
    from_username = request.form.get("from")
    to_username = request.form.get("to")
    message_text = request.form.get("message")

    try:
        con = connect("db/messages.db")
        cur = con.cursor()
    except:
        print("Connection to database failed!")

    sql = "INSERT INTO messages VALUES (?, ?, ?, ?);"
    try:
        cur.execute(sql, (
            str(uuid4()),
            from_username,
            to_username,
            message_text
        ))
        con.commit()
        flash("Message sent!")
    except Exception as e:
        flash("Can not send message! Try again!")
    return redirect("/")

@app.route("/view", methods=["POST"])
def show_messages():
    username = request.form.get("username")
    print(type(username))
    sql = "SELECT * FROM messages WHERE receiver_username=?;"

    try:
        con = connect("db/messages.db")
        cur = con.cursor()
    except:
        print("Connection to database failed!")

    try:
        res = cur.execute(sql, (
            username,
        ))
        my_messages = res.fetchall()

        return render_template("messages.html", my_messages=my_messages)
    except Exception as e:
        flash("Can not get messages! Try again!")
        return redirect("/")




app.run(debug=True)