# Trendyol Yorum Scraper

Trendyol ürünlerinin yorumlarını çeken ve PDF/Word formatında kaydeden Python web scraper aracı.

## Özellikler

- Trendyol ürün sayfasından tüm yorumları otomatik çeker
- Ürün bilgilerini (ad, marka, fiyat, puan) toplar
- Yorumları PDF formatında kaydeder
- Yorumları Word (DOCX) formatında kaydeder
- Kullanıcı dostu arayüz
- Dinamik sayfa yükleme desteği

## Kurulum

### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. Chrome Tarayıcı

Bu scraper Chrome WebDriver kullanır. Chrome tarayıcısının sisteminizde kurulu olması gerekir.
WebDriver otomatik olarak `webdriver-manager` tarafından indirilecektir.

## Kullanım

### Basit Kullanım

```bash
python trendyol_scraper.py
```

Program çalıştırıldığında:
1. Trendyol ürün URL'sini girmenizi isteyecek
2. Kayıt formatını seçmenizi isteyecek (pdf/word/both)
3. Yorumları çekip seçtiğiniz formatta kaydedecek

### Örnek URL

```
https://www.trendyol.com/marka/urun-adi-p-123456789
```

### Kod İçinde Kullanım

```python
from trendyol_scraper import TrendyolScraper

# Scraper oluştur
scraper = TrendyolScraper(headless=False)

# Ürün URL'si
url = "https://www.trendyol.com/..."

# Yorumları çek
result = scraper.scrape_product(url)

# PDF olarak kaydet
scraper.export_to_pdf("yorumlar.pdf")

# Word olarak kaydet
scraper.export_to_word("yorumlar.docx")
```

### Parametreler

**TrendyolScraper(headless=True)**
- `headless=True`: Tarayıcıyı arka planda çalıştırır (görünmez)
- `headless=False`: Tarayıcı penceresini gösterir (hata ayıklama için yararlı)

## Çıktı Formatı

### Word Dosyası
- Ürün bilgileri
- Her yorum için:
  - Kullanıcı adı
  - Puan (yıldız)
  - Tarih
  - Yorum metni

### PDF Dosyası
- Word ile aynı içerik
- Profesyonel PDF formatında

## Örnek Çıktı

Dosyalar otomatik olarak zaman damgası ile kaydedilir:
- `trendyol_yorumlar_20251015_143022.pdf`
- `trendyol_yorumlar_20251015_143022.docx`

## Önemli Notlar

1. **Robots.txt**: Bu scraper eğitim amaçlıdır. Trendyol'un kullanım koşullarına uygun kullanın.

2. **Rate Limiting**: Çok fazla istek göndermemek için kod içinde `time.sleep()` kullanılmıştır.

3. **Dinamik İçerik**: Trendyol dinamik bir site olduğu için Selenium kullanılır.

4. **Hata Yönetimi**: Scraper hata durumlarında bilgilendirici mesajlar verir.

## Sorun Giderme

### Chrome Driver Hatası
```
ChromeDriver hatası alıyorsanız, Chrome'un güncel olduğundan emin olun.
```

### Yorumlar Bulunamıyor
```
- Ürün URL'sinin doğru olduğundan emin olun
- headless=False yaparak tarayıcıyı görebilir ve hata ayıklayabilirsiniz
- Sayfanın tam yüklendiğinden emin olun
```

### Bağlantı Zaman Aşımı
```
İnternet bağlantınızı kontrol edin veya time.sleep() değerlerini artırın
```

## Geliştirme

Katkıda bulunmak isterseniz:
1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım için Trendyol'un izni gerekebilir.

## İletişim

Sorular veya öneriler için issue açabilirsiniz.
