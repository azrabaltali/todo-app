from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

gorevler = [
        {"id":1, "baslik":"Kitap oku", "tamamlandi":False},
        {"id":2, "baslik":"Spor yap", "tamamlandi":True},
        {"id":3, "baslik":"Py çalış", "tamamlandi":False}
    ]
sonraki_id = 4  #yeni görev eklerken id vermek için sayaç

@app.route("/")

def ana_sayfa():
    return render_template("index.html", gorevler = gorevler)

@app.route("/ekle", methods=["POST"])
def gorev_ekle():
    global sonraki_id

    baslik = request.form.get("baslik","").strip()

    if baslik:
        gorevler.append({
            "id": sonraki_id,
            "baslik": baslik,
            "tamamlandi": False,
        })
        sonraki_id += 1

    return redirect(url_for("ana_sayfa"))

@app.route("/tamamla/<int:gorev_id>", methods = ["POST"])
def gorev_tamamla(gorev_id):
    for gorev in gorevler:
        if gorev["id"] == gorev_id:
            gorev["tamamlandi"] = not gorev["tamamlandi"]
            break
    return redirect(url_for("ana_sayfa"))

@app.route("/sil/<int:gorev_id>", methods=["POST"])
def gorev_sil(gorev_id):
    global gorevler
    gorevler = [g for g in gorevler if g["id"] != gorev_id]
    return redirect(url_for("ana_sayfa"))


if __name__ == "__main__":
    app.run(debug=True)