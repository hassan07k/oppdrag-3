from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.htm")

@app.route("/logginn")
def logginn():
    return render_template("logginn.htm")

@app.route("/registrering")
def registrer():
    return render_template("registrering.htm")


if __name__ == '__main__':
    app.run(debug=True)