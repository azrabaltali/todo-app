# 📝 To-Do Listem

Flask ile geliştirilmiş, kullanıcı girişi destekli bir yapılacaklar listesi uygulaması.

Her kullanıcı kendi görevlerini ekleyebilir, takip edebilir ve tamamlayabilir. Görevler öncelik ve zorluk seviyelerine göre düzenlenebilir. İlerleme yüzdesi takip edilir ve gün sonunda yıldız sistemiyle bir başarı özeti sunulur.

## ✨ Özellikler

- 🔐 **Kullanıcı kaydı ve girişi:** Flask-Login ile oturum yönetimi
- 👤 **Kullanıcıya özel görevler:** Her kullanıcı yalnızca kendi görevlerini görüntüler.
- ➕ **Görev ekleme:** Başlık, açıklama, öncelik ve zorluk seviyesi belirleme
- ✅ **Görev tamamlama:** Görevleri tamamlama veya yeniden aktif hâle getirme
- 📊 **İlerleme takibi:** %0–100 arasında ilerleme ve `+10` / `−10` butonları
- 🎨 **Renkli ilerleme çubuğu:** İlerleme yüzdesine göre renk değiştiren gösterge
- 🔍 **Görev filtreleme:** Tümü, Aktif ve Tamamlanan seçenekleri
- ⭐ **Yıldız sistemi:** Görevlerin zorluk seviyesine göre yıldız kazanma
- 📈 **Gün özeti:** Toplam yıldız, başarı yüzdesi ve motivasyon mesajı
- 🌙 **Koyu tema:** Bootstrap ile desteklenen dark mode
- 🗑️ **Silme onayı:** Yanlışlıkla görev silinmesini önlemeye yardımcı onay mekanizması

## 🛠️ Kullanılan Teknolojiler

| Teknoloji        | Kullanım Amacı              |
| ---------------- | --------------------------- |
| Python 3.12      | Ana programlama dili        |
| Flask            | Web uygulaması geliştirme   |
| Flask-Login      | Kullanıcı oturum yönetimi   |
| Flask-SQLAlchemy | ORM ve veritabanı işlemleri |
| SQLite           | Veritabanı yönetimi         |
| Werkzeug         | Şifrelerin hash'lenmesi     |
| Bootstrap 5.3    | Arayüz ve koyu tema         |
| Jinja2           | HTML şablon motoru          |

## 📁 Proje Yapısı

```text
todo-app/
├── instance/
│   └── todo.db
├── templates/
│   ├── auth.html
│   ├── index.html
│   └── ozet.html
├── venv/
├── .gitignore
├── app.py
├── init_db.py
├── requirements.txt
└── README.md
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

- Python 3.10 veya üzeri
- pip
- VS Code (önerilir)

### 1. Proje klasörünü açın

VS Code üzerinden mevcut proje klasörünü açın ve **Terminal → New Terminal** seçeneğiyle terminali başlatın.

### 2. Sanal ortam oluşturun

Daha önce oluşturmadıysanız:

```bash
python -m venv venv
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. Veritabanını hazırlayın

```bash
python init_db.py
```

Bu komut, `init_db.py` dosyasında tanımlanan işlemlere göre veritabanını hazırlar ve varsa demo kullanıcı hesabını oluşturur.

### 5. Uygulamayı çalıştırın

```bash
python app.py
```

### 6. Tarayıcıda açın

[http://127.0.0.1:5000](http://127.0.0.1:5000)

Uygulamayı durdurmak için terminalde `Ctrl + C` tuşlarına basın.

Sanal ortamdan çıkmak için:

```bash
deactivate
```

## 🔑 Demo Hesap

Demo hesabı `init_db.py` dosyasında oluşturuluyorsa aşağıdaki bilgileri kullanabilirsiniz.

| Alan    | Değer           |
| ------- | --------------- |
| E-posta | `demo@demo.com` |
| Şifre   | `demo123`       |

Alternatif olarak, giriş sayfasındaki **Kayıt Ol** sekmesinden yeni bir hesap oluşturabilirsiniz.

## 📸 Kullanım

1. **Görev ekleyin:** Başlık, açıklama, öncelik ve zorluk seviyesi belirleyin.
2. **Görev durumunu değiştirin:** Tamamla veya Geri Al butonlarını kullanın.
3. **İlerlemeyi güncelleyin:** `+10` ve `−10` butonlarıyla ilerleme yüzdesini değiştirin.
4. **Görevleri filtreleyin:** Tümü, Aktif ve Tamamlanan seçeneklerini kullanın.
5. **Görev silin:** Silme butonuyla görevi kaldırın.
6. **Günlük performansınızı inceleyin:** Günü Bitir / Özet butonuyla istatistiklerinizi görüntüleyin.

## 📬 İletişim

**Geliştirici:** Azra Baltalı

**GitHub:** [@azrabaltali](https://github.com/azrabaltali)

---

