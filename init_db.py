from app import app, db, Gorev

with app.app_context():
    db.create_all()

    if Gorev.query.count() == 0:
        ilk_gorevler = [
            Gorev(baslik="Kitap oku", aciklama="Yarım saat kitap okuyacağım",
                  oncelik="normal", zorluk=1, ilerleme=0),
            Gorev(baslik="Spor yap", aciklama="30 dakika koşu",
                  oncelik="yuksek", zorluk=3, ilerleme=100, tamamlandi=True),
            Gorev(baslik="Python çalış", aciklama="Flask projesine devam",
                  oncelik="yuksek", zorluk=2, ilerleme=50),
            Gorev(baslik="Alışverişe git", aciklama="Ekmek, süt, yumurta",
                  oncelik="dusuk", zorluk=1, ilerleme=0),
        ]
        db.session.add_all(ilk_gorevler)
        db.session.commit()
        print(f"{len(ilk_gorevler)} görev eklendi.")
    else:
        print("Veritabanında zaten veri var, ekleme yapılmadı.")

    print("Veritabanı hazır.")