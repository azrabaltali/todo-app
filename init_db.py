from app import app, db, Kullanici, Gorev
from werkzeug.security import generate_password_hash

with app.app_context():
    # Önce tüm tabloları sil (temiz başlangıç)
    db.drop_all()
    db.create_all()

    # Demo kullanıcı oluştur
    demo = Kullanici(
        email="demo@demo.com",
        kullanici_adi="demo",
    )
    demo.sifre_hash = generate_password_hash("demo123")
    db.session.add(demo)
    db.session.commit()

    # Demo kullanıcıya örnek görevler ekle
    ilk_gorevler = [
        Gorev(baslik="Kitap oku", aciklama="Yarım saat kitap okuyacağım",
              oncelik="normal", zorluk=1, ilerleme=0, kullanici_id=demo.id),
        Gorev(baslik="Spor yap", aciklama="30 dakika koşu",
              oncelik="yuksek", zorluk=3, ilerleme=100, tamamlandi=True, kullanici_id=demo.id),
        Gorev(baslik="Python çalış", aciklama="Flask projesine devam",
              oncelik="yuksek", zorluk=2, ilerleme=50, kullanici_id=demo.id),
        Gorev(baslik="Alışverişe git", aciklama="Ekmek, süt, yumurta",
              oncelik="dusuk", zorluk=1, ilerleme=0, kullanici_id=demo.id),
    ]
    db.session.add_all(ilk_gorevler)
    db.session.commit()

    print(f"Demo kullanıcı oluşturuldu: {demo.email} / demo123")
    print(f"{len(ilk_gorevler)} görev eklendi.")
    print("Veritabanı hazır.")