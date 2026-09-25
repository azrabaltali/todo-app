from app import app, db, Gorev

with app.app_context():
    db.create_all()

    # Zaten veri varsa tekrar ekleme
    if Gorev.query.count() == 0:
        ilk_gorevler = [
            Gorev(baslik="Kitap oku"),
            Gorev(baslik="Spor yap", tamamlandi=True),
            Gorev(baslik="Python çalış"),
        ]
        db.session.add_all(ilk_gorevler)
        db.session.commit()
        print(f"{len(ilk_gorevler)} görev eklendi.")
    else:
        print("Veritabanında zaten veri var, ekleme yapılmadı.")

    print("Veritabanı hazır.")