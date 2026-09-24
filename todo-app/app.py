from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def ana_sayfa():
    gorevler = ["Kitap oku", "Spor yap", "Python çalış"]
    return render_template("index.html", gorevler = gorevler)

if __name__ == "__main__":
    app.run(debug=True)