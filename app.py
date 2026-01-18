from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
import urllib.parse

app = Flask(__name__)

# 🔐 MongoDB credentials (encode password)
username = "anshutamrakar69_db_user"
password = urllib.parse.quote_plus("An!sh@1999")

# ✅ Correct MongoDB Atlas URI (NO SPACE, TLS enabled)
MONGO_URI = (
    f"mongodb+srv://{username}:{password}"
    "@cluster0.do2hzyz.mongodb.net/testdb"
    "?retryWrites=true&w=majority&tls=true"
)

# ✅ Mongo Client with TLS fix
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["testdb"]
collection = db["users"]

# ---------- API Route ----------
@app.route("/api")
def api_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

# ---------- Form Route ----------
@app.route("/", methods=["GET", "POST"])
def form():
    error = None
    if request.method == "POST":
        try:
            collection.insert_one({
                "name": request.form["name"],
                "email": request.form["email"]
            })
            return redirect(url_for("success"))
        except Exception as e:
            error = str(e)

    return render_template("form.html", error=error)

# ---------- Success Route ----------
@app.route("/success")
def success():
    return render_template("success.html")

# ---------- Run App ----------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
