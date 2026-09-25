from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)