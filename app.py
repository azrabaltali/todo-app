from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Gorev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text, default="")
    oncelik = db.Column(db.String(10), default="normal")
    zorluk = db.Column(db.Integer, default=1)
    ilerleme = db.Column(db.Integer, default=0)
    tamamlandi = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Gorev {self.id}: {self.baslik}>"


@app.route("/")
def ana_sayfa():
    gorevler = Gorev.query.all()
    return render_template("index.html", gorevler=gorevler)


@app.route("/ekle", methods=["POST"])
def gorev_ekle():
    baslik = request.form.get("baslik", "").strip()
    aciklama = request.form.get("aciklama", "").strip()
    oncelik = request.form.get("oncelik", "normal")
    zorluk = request.form.get("zorluk", "1")

    if baslik:
        yeni_gorev = Gorev(
            baslik=baslik,
            aciklama=aciklama,
            oncelik=oncelik,
            zorluk=int(zorluk),
        )
        db.session.add(yeni_gorev)
        db.session.commit()

    return redirect(url_for("ana_sayfa"))


@app.route("/tamamla/<int:gorev_id>", methods=["POST"])
def gorev_tamamla(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    gorev.tamamlandi = not gorev.tamamlandi
    db.session.commit()
    return redirect(url_for("ana_sayfa"))


@app.route("/sil/<int:gorev_id>", methods=["POST"])
def gorev_sil(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    db.session.delete(gorev)
    db.session.commit()
    return redirect(url_for("ana_sayfa"))


@app.route("/ilerleme/<int:gorev_id>", methods=["POST"])
def gorev_ilerleme(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    degisim = int(request.form.get("degisim", 0))

    yeni_deger = gorev.ilerleme + degisim

    # 0-100 arasında sınırla
    if yeni_deger < 0:
        yeni_deger = 0
    elif yeni_deger > 100:
        yeni_deger = 100

    gorev.ilerleme = yeni_deger

    # İlerleme %100 olduysa otomatik tamamlandı işaretle
    if yeni_deger == 100:
        gorev.tamamlandi = True

    db.session.commit()
    return redirect(url_for("ana_sayfa"))


@app.route("/ozet")
def ozet():
    tum_gorevler = Gorev.query.all()

    toplam_gorev = len(tum_gorevler)
    tamamlanan = [g for g in tum_gorevler if g.tamamlandi]
    tamamlanan_sayi = len(tamamlanan)

    # Tamamlanan görevlerin zorluk puanlarını topla
    kazanilan_yildiz = sum(g.zorluk for g in tamamlanan)

    # Maksimum olası yıldız (hepsi tamamlansaydı)
    maksimum_yildiz = sum(g.zorluk for g in tum_gorevler)

    # Yüzde (0'a bölme hatasına karşı)
    if maksimum_yildiz > 0:
        basari_yuzdesi = round((kazanilan_yildiz / maksimum_yildiz) * 100)
    else:
        basari_yuzdesi = 0

    return render_template(
        "ozet.html",
        toplam_gorev=toplam_gorev,
        tamamlanan_sayi=tamamlanan_sayi,
        kazanilan_yildiz=kazanilan_yildiz,
        maksimum_yildiz=maksimum_yildiz,
        basari_yuzdesi=basari_yuzdesi,
        tamamlanan=tamamlanan,
    )


if __name__ == "__main__":
    app.run(debug=True)