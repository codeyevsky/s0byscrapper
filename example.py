"""
Trendyol Scraper Kullanım Örnekleri
"""

from trendyol_scraper import TrendyolScraper
from datetime import datetime


def example_1_basic():
    """
    Örnek 1: Temel kullanım
    Bir ürünün yorumlarını çek ve hem PDF hem Word olarak kaydet
    """
    print("=" * 60)
    print("ÖRNEK 1: Temel Kullanım")
    print("=" * 60)

    # Ürün URL'si
    url = "https://www.trendyol.com/casio/erkek-kol-saati-mtp-1302d-1avdf-p-3800237"

    # Scraper oluştur (tarayıcı görünür modda)
    scraper = TrendyolScraper(headless=False)

    # Yorumları çek
    result = scraper.scrape_product(url)

    # Sonuçları göster
    print(f"\nÜrün: {result['product_info'].get('name')}")
    print(f"Marka: {result['product_info'].get('brand')}")
    print(f"Toplam {result['total_comments']} yorum çekildi\n")

    # Zaman damgası ile dosya adı oluştur
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # PDF olarak kaydet
    scraper.export_to_pdf(f"yorumlar_{timestamp}.pdf")

    # Word olarak kaydet
    scraper.export_to_word(f"yorumlar_{timestamp}.docx")

    print("İşlem tamamlandı!")


def example_2_headless():
    """
    Örnek 2: Arka planda çalıştırma (headless mode)
    Tarayıcı görünmeden yorumları çek
    """
    print("=" * 60)
    print("ÖRNEK 2: Arka Plan Modu (Headless)")
    print("=" * 60)

    url = input("Trendyol ürün URL'sini girin: ")

    # Scraper oluştur (arka plan modunda)
    scraper = TrendyolScraper(headless=True)

    # Yorumları çek
    result = scraper.scrape_product(url)

    print(f"\n{result['total_comments']} yorum çekildi")

    # Sadece PDF olarak kaydet
    scraper.export_to_pdf("yorumlar.pdf")
    print("PDF kaydedildi!")


def example_3_multiple_products():
    """
    Örnek 3: Birden fazla ürün
    Birden fazla ürünün yorumlarını sırayla çek
    """
    print("=" * 60)
    print("ÖRNEK 3: Birden Fazla Ürün")
    print("=" * 60)

    urls = [
        "https://www.trendyol.com/product-1",
        "https://www.trendyol.com/product-2",
        # Daha fazla URL ekleyebilirsiniz
    ]

    for idx, url in enumerate(urls, 1):
        print(f"\n[{idx}/{len(urls)}] İşleniyor: {url}")

        scraper = TrendyolScraper(headless=True)

        try:
            result = scraper.scrape_product(url)

            # Her ürün için ayrı dosya oluştur
            product_name = result['product_info'].get('name', f'urun_{idx}')
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_'))[:50]

            scraper.export_to_pdf(f"{safe_name}.pdf")
            print(f"✓ {result['total_comments']} yorum kaydedildi")

        except Exception as e:
            print(f"✗ Hata: {str(e)}")


def example_4_custom_analysis():
    """
    Örnek 4: Yorum analizi
    Yorumları çektikten sonra özel analiz yap
    """
    print("=" * 60)
    print("ÖRNEK 4: Yorum Analizi")
    print("=" * 60)

    url = input("Trendyol ürün URL'sini girin: ")

    scraper = TrendyolScraper(headless=True)
    result = scraper.scrape_product(url)

    comments = result['comments']

    if not comments:
        print("Yorum bulunamadı!")
        return

    # İstatistikler
    print(f"\n{'='*60}")
    print("İSTATİSTİKLER")
    print(f"{'='*60}")

    # Toplam yorum
    print(f"Toplam Yorum: {len(comments)}")

    # Puan dağılımı
    ratings = {}
    for comment in comments:
        rating = comment.get('rating', 'N/A')
        ratings[rating] = ratings.get(rating, 0) + 1

    print("\nPuan Dağılımı:")
    for rating, count in sorted(ratings.items(), reverse=True):
        percentage = (count / len(comments)) * 100
        print(f"  {rating} yıldız: {count} yorum ({percentage:.1f}%)")

    # Ortalama yorum uzunluğu
    total_length = sum(len(c.get('comment', '')) for c in comments)
    avg_length = total_length / len(comments) if comments else 0
    print(f"\nOrtalama Yorum Uzunluğu: {avg_length:.0f} karakter")

    # En uzun yorum
    longest = max(comments, key=lambda x: len(x.get('comment', '')))
    print(f"En Uzun Yorum: {len(longest.get('comment', ''))} karakter")

    # En kısa yorum
    shortest = min(comments, key=lambda x: len(x.get('comment', '')) if x.get('comment') else float('inf'))
    print(f"En Kısa Yorum: {len(shortest.get('comment', ''))} karakter")

    # Dosyaya kaydet
    scraper.export_to_pdf("analiz_raporu.pdf")
    print("\nRapor 'analiz_raporu.pdf' olarak kaydedildi!")


def example_5_filter_comments():
    """
    Örnek 5: Yorumları filtrele
    Sadece belirli kriterlere uyan yorumları kaydet
    """
    print("=" * 60)
    print("ÖRNEK 5: Yorum Filtreleme")
    print("=" * 60)

    url = input("Trendyol ürün URL'sini girin: ")

    scraper = TrendyolScraper(headless=True)
    result = scraper.scrape_product(url)

    # Orijinal yorumları sakla
    all_comments = scraper.comments.copy()

    # Sadece 5 yıldızlı yorumları filtrele
    scraper.comments = [c for c in all_comments if c.get('rating') == '5']
    print(f"\n5 yıldızlı yorumlar: {len(scraper.comments)}")
    scraper.export_to_pdf("5_yildiz.pdf")

    # Sadece 1-2 yıldızlı yorumları filtrele
    scraper.comments = [c for c in all_comments if c.get('rating') in ['1', '2']]
    print(f"1-2 yıldızlı yorumlar: {len(scraper.comments)}")
    scraper.export_to_pdf("dusuk_puan.pdf")

    # Uzun yorumları filtrele (100 karakterden fazla)
    scraper.comments = [c for c in all_comments if len(c.get('comment', '')) > 100]
    print(f"Detaylı yorumlar (100+ karakter): {len(scraper.comments)}")
    scraper.export_to_word("detayli_yorumlar.docx")

    print("\nFiltrelenmiş yorumlar kaydedildi!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TRENDYOL SCRAPER KULLANIM ÖRNEKLERİ")
    print("="*60)
    print("\nHangi örneği çalıştırmak istersiniz?")
    print("1. Temel kullanım (PDF ve Word export)")
    print("2. Arka plan modu (Headless)")
    print("3. Birden fazla ürün")
    print("4. Yorum analizi ve istatistikler")
    print("5. Yorumları filtrele")
    print("0. Çıkış")

    choice = input("\nSeçiminiz (0-5): ")

    if choice == "1":
        example_1_basic()
    elif choice == "2":
        example_2_headless()
    elif choice == "3":
        example_3_multiple_products()
    elif choice == "4":
        example_4_custom_analysis()
    elif choice == "5":
        example_5_filter_comments()
    elif choice == "0":
        print("Çıkılıyor...")
    else:
        print("Geçersiz seçim!")
