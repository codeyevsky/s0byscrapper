# 🎯 Trendyol Scraper - Son Kullanıcı için Rehber

## Python Olmayan Bilgisayarlarda Nasıl Çalışır?

### 🚀 Yöntem 1: EXE Dosyası (ÖNERİLEN - EN KOLAY)

#### Geliştirici İçin (Senin Yapman Gerekenler):

1. **PyInstaller'ı yükle:**
```bash
pip install pyinstaller
```

2. **EXE oluştur - İki seçenek:**

**A) Otomatik (Önerilen):**
```bash
python build_exe.py
```

**B) Manuel:**
```bash
build_exe_simple.bat
```
(veya dosyaya çift tıkla)

3. **Sonuç:**
- `dist/TrendyolScraper.exe` dosyası oluşacak
- Bu dosya **10-50 MB** civarı olacak (tüm bağımlılıklar dahil)
- Bu tek dosyayı kullanıcılara gönderebilirsin

#### Son Kullanıcı İçin (Kullanacak Kişiler):

1. `TrendyolScraper.exe` dosyasını al
2. Dosyaya çift tıkla
3. GUI açılacak, kullan!

**Gereksinimler:**
- ✅ Python **GEREKMEZ**
- ✅ Kütüphane kurulumu **GEREKMEZ**
- ⚠️ Chrome tarayıcı **GEREKLİ** (zaten çoğu bilgisayarda var)
- ⚠️ Windows 10/11 (test edildi)

---

### 🐍 Yöntem 2: Python Kurulumlu Kullanım

Eğer Python yüklemek istiyorlarsa:

#### Adım 1: Python Yükle
1. https://www.python.org/downloads/ adresine git
2. "Download Python 3.x" butonuna tıkla
3. Kurulumda **"Add Python to PATH"** kutucuğunu işaretle ✅
4. Install Now

#### Adım 2: Projeyi İndir
1. Proje klasörünü kullanıcıya gönder
2. ZIP olarak gönderebilirsin

#### Adım 3: Kütüphaneleri Yükle
Proje klasöründe terminal/cmd aç:
```bash
pip install -r requirements.txt
```

#### Adım 4: Çalıştır
```bash
python gui_scraper.py
```
veya `run_gui.bat` dosyasına çift tıkla

---

## 📊 Karşılaştırma

| Özellik | EXE Yöntemi | Python Yöntemi |
|---------|-------------|----------------|
| Python gerekli mi? | ❌ HAYIR | ✅ EVET |
| Kurulum süresi | 0 dakika | 5-10 dakika |
| Dosya boyutu | 10-50 MB (tek dosya) | 5 MB (çok dosya) |
| Kullanım kolaylığı | ⭐⭐⭐⭐⭐ Çok kolay | ⭐⭐⭐ Orta |
| Güncelleme | Yeni .exe gönder | Git pull / ZIP indir |
| Önerilen kullanıcı | Teknik bilgisi olmayan | Geliştiriciler |

---

## 🎯 Önerim

**Teknik bilgisi olmayan kullanıcılar için:**
→ **EXE yöntemini kullan**
→ Tek dosya gönder, bitsin gitsin
→ "Python nedir?" sorularıyla uğraşma

**Geliştiriciler veya öğrenmek isteyenler için:**
→ Python yöntemini kullan
→ Kodu görebilirler, öğrenebilirler
→ Katkıda bulunabilirler

---

## ⚠️ Önemli Notlar

1. **Chrome Tarayıcı:**
   - Her iki yöntemde de Chrome yüklü olmalı
   - Selenium Chrome'u kullanarak scraping yapıyor
   - https://www.google.com/chrome/

2. **Antivirüs Uyarısı:**
   - EXE dosyası bazı antivirüslerde uyarı verebilir
   - Güvenli ama "bilinmeyen geliştirici" olduğu için
   - Kullanıcıya "Allow/İzin ver" demesini söyle

3. **İlk Çalışma:**
   - İlk çalıştırmada ChromeDriver indirebilir
   - İnternet bağlantısı gerekli

---

## 🔧 Sorun Giderme

**"Python bulunamadı" hatası:**
→ EXE versiyonunu kullan veya Python'u PATH'e ekle

**"Chrome driver hatası":**
→ Chrome güncel mi kontrol et
→ İnternet bağlantısı var mı?

**"Modül bulunamadı" hatası:**
→ `pip install -r requirements.txt` çalıştır
→ Veya EXE versiyonunu kullan

**EXE çok yavaş çalışıyor:**
→ Normal, ilk açılış yavaş olabilir
→ Tüm kütüphaneler açılıp hafızaya yükleniyor

---

## 📞 Destek

Sorun yaşarsan:
1. Chrome'un güncel olduğundan emin ol
2. İnternet bağlantısını kontrol et
3. Antivirüsü geçici olarak kapat ve dene
4. Hata mesajını not al ve ilet

---

## 🎉 Başarılı Kurulum Testi

GUI açıldığında şunları göreceksin:
- Mavi temalı pencere
- Sol tarafta kontroller
- Sağ tarafta log alanı
- "● Hazır" yazısı

Bu görüntü varsa kurulum başarılı! ✅
