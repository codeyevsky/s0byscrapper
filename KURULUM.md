# Trendyol Scraper - Kurulum Rehberi

## 📦 Kurulum Seçenekleri

### Seçenek 1: Tam Kurulum (Önerilen)
Tüm kütüphaneleri yükler (gelecekte kullanılabilecek araçlar dahil):

```bash
pip install -r requirements.txt
```

### Seçenek 2: Minimal Kurulum
Sadece projenin çalışması için gerekli kütüphaneleri yükler:

```bash
pip install -r requirements-minimal.txt
```

## ✅ Hangi Kütüphaneler Mutlaka Gerekli?

| Kütüphane | Neden Gerekli? | Olmadan Çalışır mı? |
|-----------|----------------|---------------------|
| **selenium** | Web scraping için | ❌ HAYIR - Mutlaka gerekli |
| **python-docx** | Word dosyası oluşturmak için | ❌ HAYIR - Export çalışmaz |
| **reportlab** | PDF dosyası oluşturmak için | ❌ HAYIR - Export çalışmaz |
| beautifulsoup4 | HTML parsing (kullanılmıyor) | ✅ EVET - Şu an gereksiz |
| requests | HTTP istekleri (kullanılmıyor) | ✅ EVET - Şu an gereksiz |
| webdriver-manager | ChromeDriver otomatik kurulum | ✅ EVET - Manuel kurulumla çalışır |
| lxml | XML/HTML parser | ✅ EVET - Şu an gereksiz |

## 🎯 Önerim

**Başkalarıyla paylaşacaksan:**
- **requirements.txt** kullan (tam kurulum)
- Gelecekte özellik eklerseniz bu kütüphaneler işe yarayabilir
- Disk alanı çok önemli değilse tam kurulum daha güvenli

**Minimal sistem için:**
- **requirements-minimal.txt** kullan
- Sadece 3 kütüphane yükler
- Daha hızlı kurulum, daha az disk alanı

## 🚀 Hızlı Test

Kurulumdan sonra test etmek için:

```bash
python gui_scraper.py
```

Eğer GUI açılırsa kurulum başarılı! ✅

## 📝 Not

- **tkinter**, **datetime**, **json**, **time**, **threading**, **sys**, **io** → Python ile birlikte gelir, yüklemeye gerek yok
- Chrome tarayıcı sisteminizde yüklü olmalı (Selenium için)
