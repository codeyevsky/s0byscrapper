# Trendyol Scraper

Trendyol'dan ürün yorumlarını ve mağaza değerlendirmelerini çekerek Word formatında kaydeden Python tabanlı web scraper.

## Özellikler

- **Grafik Arayüz (GUI):** Kullanıcı dostu modern arayüz
- **2 Farklı Scraping Modu:**
  - Ürün Yorumları
  - Mağaza Değerlendirmeleri (alfabetik kategorize)
- **Infinite Scroll:** Tüm yorumları/değerlendirmeleri otomatik yükler
- **Word Export:** Düzenli formatlanmış Word dosyası
- **Real-time Log:** Canlı işlem takibi
- **Headless Mode:** Arka planda çalıştırma seçeneği

## Kurulum

### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Chrome Tarayıcı

Bu scraper Chrome WebDriver kullanır. Chrome tarayıcısının sisteminizde kurulu olması gerekir.
WebDriver otomatik olarak `webdriver-manager` tarafından indirilecektir.

## Kullanım

### GUI ile Kullanım (Önerilen)

```bash
python gui_app.py
```

**Arayüz Özellikleri:**
1. **Scraping Modu Seçimi:** Radio button ile mod seçin
2. **URL Girişi:** Trendyol ürün URL'sini yapıştırın
3. **Maksimum Limit:** İsteğe bağlı sayı limiti
4. **Headless Mode:** Tarayıcıyı gizli çalıştırma
5. **Real-time Log:** Canlı işlem takibi
6. **Progress Bar:** Görsel ilerleme göstergesi

### Komut Satırı ile Kullanım

```bash
python trendyol_scraper.py
```

Adımlar:
1. Mod seçin (1: Ürün Yorumları, 2: Mağaza Değerlendirmeleri)
2. URL girin
3. Limit belirleyin (opsiyonel)

### Programatik Kullanım

```python
from trendyol_scraper import TrendyolScraper

scraper = TrendyolScraper(headless=False, max_comments=50)

result = scraper.scrape_product(
    url="https://www.trendyol.com/...",
    scrape_mode='reviews'  # veya 'comments'
)

scraper.export_to_word("output.docx")

print(f"Çekilen: {result.get('total_reviews', result.get('total_comments'))}")
```

## Çıktı Formatı

### Ürün Yorumları
```
Trendyol Ürün Yorumları
├── Ürün Bilgileri
├── Toplam Yorum Sayısı: X
└── Yorumlar
    ├── Yorum #1 (Kullanıcı, Tarih, Metin)
    └── ...
```

### Mağaza Değerlendirmeleri (Alfabetik)
```
Trendyol Ürün Değerlendirmeleri
├── Ürün Bilgileri
├── Toplam Değerlendirme Sayısı: X
└── Değerlendirmeler (Alfabetik)
    ├── 📦 Asus Laptop
    │   └── 5 değerlendirme
    ├── 📦 Samsung Monitor
    └── ...
```

**Dosya Adı:**
- `trendyol_comments_20251015_143022.docx`
- `trendyol_reviews_20251015_143022.docx`

## GUI Ekran Görüntüsü

```
┌─────────────────────────────────────────┐
│      Trendyol Scraper                   │
├─────────────────────────────────────────┤
│ Scraping Modu:                          │
│  ○ Ürün Yorumları                       │
│  ○ Mağaza Değerlendirmeleri             │
│                                         │
│ Trendyol URL:                           │
│ [___________________________________]   │
│                                         │
│ Maksimum Sayı:                          │
│ [________]                              │
│                                         │
│ ☐ Arka planda çalıştır                 │
│                                         │
│ [Başlat]  [Durdur]                      │
│                                         │
│ İlerleme:                               │
│ [████████████████░░░░░░░░]              │
│                                         │
│ Log:                                    │
│ ┌───────────────────────────────┐       │
│ │ [12:34:56] Scraper başlatıldı │       │
│ │ [12:34:58] 25 yorum çekildi    │       │
│ └───────────────────────────────┘       │
│                                         │
│ ● Hazır                                 │
└─────────────────────────────────────────┘
```

## Teknik Detaylar

| Özellik | Açıklama |
|---------|----------|
| GUI Framework | Tkinter |
| Web Scraping | Selenium + Chrome WebDriver |
| Scroll Yöntemi | Infinite Scroll (max 200) |
| Export Format | Word (DOCX) |
| Threading | Arka plan thread ile GUI donmaması |

## Sorun Giderme

**ChromeDriver Hatası:**
- Chrome tarayıcısını güncelleyin

**Element Bulunamadı:**
- Sayfa yapısı değişmiş olabilir

**GUI Açılmıyor:**
- `tkinter` kütüphanesinin kurulu olduğundan emin olun

**Hedef Sayıya Ulaşılamadı:**
- Normal bir durum, sayfada yeterli veri yok

## Katkıda Bulunma

1. Fork edin
2. Branch oluşturun (`git checkout -b feature/amazing`)
3. Commit edin (`git commit -m 'Add feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

## Lisans

MIT License - Eğitim amaçlıdır

## İletişim

Issue açarak soru sorabilirsiniz

---

**⚠ Uyarı:** Trendyol'un web yapısı değişebilir. Selector'ların güncellenmesi gerekebilir.
