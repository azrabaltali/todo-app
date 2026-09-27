from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Gorev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
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

    if baslik:
        yeni_gorev = Gorev(baslik=baslik)
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


if __name__ == "__main__":
    app.run(debug=True)