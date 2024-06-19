from flask import Flask, render_template

app = Flask(__name__)

@app.route("/index")
def home():
    return render_template("template/index.html")

@app.route("/manage")
def manage():
    return render_template("template/manage.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
