from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "cok-gizli-bir-anahtar-bunu-sonra-degistir"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth"
login_manager.login_message = "Bu sayfayı görmek için giriş yapmalısın."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return Kullanici.query.get(int(user_id))


class Kullanici(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    kullanici_adi = db.Column(db.String(50), unique=True, nullable=False)
    sifre_hash = db.Column(db.String(200), nullable=False)

    gorevler = db.relationship("Gorev", backref="sahip", lazy=True)

    def __repr__(self):
        return f"<Kullanici {self.kullanici_adi}>"


class Gorev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text, default="")
    oncelik = db.Column(db.String(10), default="normal")
    zorluk = db.Column(db.Integer, default=1)
    ilerleme = db.Column(db.Integer, default=0)
    tamamlandi = db.Column(db.Boolean, default=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey("kullanici.id"), nullable=False)

    def __repr__(self):
        return f"<Gorev {self.id}: {self.baslik}>"


# ---------------------- AUTH (GİRİŞ + KAYIT) ---------------------- #

@app.route("/auth", methods=["GET", "POST"])
def auth():
    aktif_sekme = request.form.get("form_tipi", "giris")  # POST'ta hangi form gönderildi

    if request.method == "POST":
        if aktif_sekme == "kayit":
            # --- KAYIT İŞLEMİ ---
            email = request.form.get("email", "").strip().lower()
            kullanici_adi = request.form.get("kullanici_adi", "").strip()
            sifre = request.form.get("sifre", "")
            sifre_tekrar = request.form.get("sifre_tekrar", "")

            hata = None

            if not email or not kullanici_adi or not sifre:
                hata = "Tüm alanlar zorunludur."
            elif len(sifre) < 6:
                hata = "Şifre en az 6 karakter olmalıdır."
            elif sifre != sifre_tekrar:
                hata = "Şifreler eşleşmiyor."
            elif Kullanici.query.filter_by(email=email).first():
                hata = "Bu email zaten kayıtlı."
            elif Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first():
                hata = "Bu kullanıcı adı zaten alınmış."

            if hata:
                return render_template("auth.html", aktif_sekme="kayit",
                                       hata=hata, email=email,
                                       kullanici_adi=kullanici_adi)

            yeni_kullanici = Kullanici(
                email=email,
                kullanici_adi=kullanici_adi,
                sifre_hash=generate_password_hash(sifre),
            )
            db.session.add(yeni_kullanici)
            db.session.commit()

            flash("Kayıt başarılı! Şimdi giriş yapabilirsin.", "success")
            return redirect(url_for("auth"))

        else:
            # --- GİRİŞ İŞLEMİ ---
            email = request.form.get("email", "").strip().lower()
            sifre = request.form.get("sifre", "")

            kullanici = Kullanici.query.filter_by(email=email).first()

            if not kullanici or not check_password_hash(kullanici.sifre_hash, sifre):
                hata = "Email veya şifre hatalı."
                return render_template("auth.html", aktif_sekme="giris",
                                       hata=hata, email=email)

            login_user(kullanici)
            return redirect(url_for("ana_sayfa"))

    # GET isteği → formu göster
    return render_template("auth.html", aktif_sekme=aktif_sekme)


@app.route("/cikis")
def cikis():
    logout_user()
    return redirect(url_for("auth"))

# ---------------------- GÖREV ROUTE'LARI ---------------------- #

@app.route("/")
@login_required
def ana_sayfa():
    gorevler = Gorev.query.filter_by(kullanici_id=current_user.id).all()
    return render_template("index.html", gorevler=gorevler)


@app.route("/ekle", methods=["POST"])
@login_required
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
            kullanici_id=current_user.id,
        )
        db.session.add(yeni_gorev)
        db.session.commit()

    return redirect(url_for("ana_sayfa"))


@app.route("/tamamla/<int:gorev_id>", methods=["POST"])
@login_required
def gorev_tamamla(gorev_id):
    gorev = Gorev.query.filter_by(id=gorev_id, kullanici_id=current_user.id).first_or_404()
    gorev.tamamlandi = not gorev.tamamlandi
    db.session.commit()
    return redirect(url_for("ana_sayfa"))


@app.route("/sil/<int:gorev_id>", methods=["POST"])
@login_required
def gorev_sil(gorev_id):
    gorev = Gorev.query.filter_by(id=gorev_id, kullanici_id=current_user.id).first_or_404()
    db.session.delete(gorev)
    db.session.commit()
    return redirect(url_for("ana_sayfa"))


@app.route("/ilerleme/<int:gorev_id>", methods=["POST"])
@login_required
def gorev_ilerleme(gorev_id):
    gorev = Gorev.query.filter_by(id=gorev_id, kullanici_id=current_user.id).first_or_404()
    degisim = int(request.form.get("degisim", 0))

    yeni_deger = gorev.ilerleme + degisim

    if yeni_deger < 0:
        yeni_deger = 0
    elif yeni_deger > 100:
        yeni_deger = 100

    gorev.ilerleme = yeni_deger

    if yeni_deger == 100:
        gorev.tamamlandi = True

    db.session.commit()
    return redirect(url_for("ana_sayfa"))


@app.route("/ozet")
@login_required
def ozet():
    tum_gorevler = Gorev.query.filter_by(kullanici_id=current_user.id).all()

    toplam_gorev = len(tum_gorevler)
    tamamlanan = [g for g in tum_gorevler if g.tamamlandi]
    tamamlanan_sayi = len(tamamlanan)

    kazanilan_yildiz = sum(g.zorluk for g in tamamlanan)
    maksimum_yildiz = sum(g.zorluk for g in tum_gorevler)

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