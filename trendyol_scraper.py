import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black
from datetime import datetime


class TrendyolScraper:
    def __init__(self, headless=False, max_comments=None):
        """
        Trendyol scraper başlatıcı

        Args:
            headless (bool): Tarayıcıyı arka planda çalıştırma
            max_comments (int): Maksimum çekilecek yorum sayısı (None = tümü)
        """
        self.driver = None
        self.headless = headless
        self.max_comments = max_comments
        self.comments = []
        self.product_info = {}

    def setup_driver(self):
        """Selenium WebDriver ayarları - Selenium Manager otomatik driver indirir"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Selenium 4.6+ otomatik driver yönetimi kullanır
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def scrape_product(self, url):
        """
        Ürün bilgilerini ve yorumları çeker

        Args:
            url (str): Trendyol ürün URL'si

        Returns:
            dict: Ürün bilgileri ve yorumlar
        """
        try:
            self.setup_driver()
            print(f"URL açılıyor: {url}")
            self.driver.get(url)

            # Sayfanın yüklenmesini bekle
            time.sleep(3)

            # Ürün bilgilerini al
            self._extract_product_info()

            # Yorumlar sekmesine git
            self._navigate_to_comments()

            # Yorumları çek
            self._extract_comments()

            return {
                'product_info': self.product_info,
                'comments': self.comments,
                'total_comments': len(self.comments)
            }

        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

    def _extract_json_ld(self):
        """Sayfadaki JSON-LD verilerini çeker"""
        try:
            script_tags = self.driver.find_elements(By.CSS_SELECTOR, 'script[type="application/ld+json"]')
            json_ld_data = []

            for script in script_tags:
                try:
                    data = json.loads(script.get_attribute('innerHTML'))
                    json_ld_data.append(data)
                except json.JSONDecodeError:
                    continue

            return json_ld_data
        except Exception as e:
            print(f"JSON-LD çekilirken hata: {str(e)}")
            return []

    def _extract_product_info(self):
        """Ürün bilgilerini JSON-LD'den çeker"""
        try:
            # JSON-LD verilerini al
            json_ld_data = self._extract_json_ld()

            # Product verilerini bul
            product_data = None
            for data in json_ld_data:
                if isinstance(data, dict) and data.get('@type') == 'Product':
                    product_data = data
                    break

            if product_data:
                # Ürün adı
                self.product_info['name'] = product_data.get('name', 'Ürün adı bulunamadı')

                # Puan
                rating_data = product_data.get('aggregateRating', {})
                if isinstance(rating_data, dict):
                    rating_value = rating_data.get('ratingValue', 'N/A')
                    rating_count = rating_data.get('ratingCount', 0)
                    self.product_info['rating'] = f"{rating_value} ({rating_count} değerlendirme)"
                else:
                    self.product_info['rating'] = 'Puan bulunamadı'

                print(f"Ürün bilgisi: {self.product_info['name']}")
            else:
                # Fallback: CSS selector kullan
                print("JSON-LD'de ürün bulunamadı, CSS selector kullanılıyor...")
                self._extract_product_info_fallback()

        except Exception as e:
            print(f"Ürün bilgisi çekilirken hata: {str(e)}")
            self._extract_product_info_fallback()

    def _extract_product_info_fallback(self):
        """Ürün bilgilerini CSS selector ile çeker (fallback)"""
        try:
            # Ürün adı - info-title-row class'ından
            try:
                # Önce info-title-row class'ını dene
                title_row = self.driver.find_element(By.CSS_SELECTOR, ".info-title-row, [class*='info-title-row']")

                # Ürün adı (başlık)
                try:
                    product_name = title_row.find_element(By.CSS_SELECTOR, "h1, [class*='title']").text
                    self.product_info['name'] = product_name
                except:
                    self.product_info['name'] = title_row.text.split('\n')[0] if title_row.text else "Ürün adı bulunamadı"

            except:
                # info-title-row bulunamazsa, eski selector'ları dene
                try:
                    product_name = self.driver.find_element(By.CSS_SELECTOR, "h1.pr-new-br, h1").text
                    self.product_info['name'] = product_name
                except:
                    self.product_info['name'] = "Ürün adı bulunamadı"

            # Puan - rate class'ından
            try:
                rating = self.driver.find_element(By.CSS_SELECTOR, ".rate, [class*='rate'], div.rating-score span, span[class*='rating']").text
                self.product_info['rating'] = rating
            except:
                self.product_info['rating'] = "Puan bulunamadı"

            print(f"Ürün bilgisi (fallback): {self.product_info['name']}")

        except Exception as e:
            print(f"Ürün bilgisi (fallback) çekilirken hata: {str(e)}")

    def _navigate_to_comments(self):
        """Yorumlar bölümüne gider"""
        try:
            # Sayfayı aşağı kaydır
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)

            # Yorumlar sekmesini bul ve tıkla
            try:
                # Çeşitli selector'ları dene
                possible_selectors = [
                    "//a[contains(@href, '#comments')]",
                    "//div[contains(text(), 'Değerlendirmeler')]",
                    "//button[contains(text(), 'Değerlendirmeler')]",
                    "//a[contains(text(), 'Yorumlar')]"
                ]

                clicked = False
                for selector in possible_selectors:
                    try:
                        comments_tab = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        self.driver.execute_script("arguments[0].click();", comments_tab)
                        time.sleep(2)
                        print("Yorumlar sekmesine geçildi")
                        clicked = True
                        break
                    except:
                        continue

                if not clicked:
                    print("Yorumlar sekmesi bulunamadı, JSON-LD'den yorumlar çekilecek")

            except Exception as e:
                print(f"Yorumlar sekmesi hatası: {str(e)}")

        except Exception as e:
            print(f"Yorumlar bölümüne geçilirken hata: {str(e)}")

    def _extract_comments(self):
        """Tüm yorumları çeker - önce JSON-LD'den, sonra HTML'den"""
        try:
            print("Yorumlar çekiliyor...")

            # Önce JSON-LD'den yorumları çekmeyi dene
            json_ld_data = self._extract_json_ld()

            # Review verilerini bul
            reviews_found = False
            for data in json_ld_data:
                if isinstance(data, dict):
                    # Product içindeki review'ları kontrol et
                    if data.get('@type') == 'Product' and 'review' in data:
                        reviews = data.get('review', [])
                        if not isinstance(reviews, list):
                            reviews = [reviews]

                        for review in reviews:
                            # Maksimum yorum sayısına ulaşıldıysa dur
                            if self.max_comments and len(self.comments) >= self.max_comments:
                                print(f"Maksimum yorum sayısına ({self.max_comments}) ulaşıldı")
                                break

                            if isinstance(review, dict) and review.get('@type') == 'Review':
                                comment_data = {}

                                # Kullanıcı adı
                                author = review.get('author', {})
                                if isinstance(author, dict):
                                    comment_data['user'] = author.get('name', 'Anonim')
                                else:
                                    comment_data['user'] = str(author) if author else 'Anonim'

                                # Yorum metni
                                comment_data['comment'] = review.get('reviewBody', '')

                                # Tarih
                                date_published = review.get('datePublished', '')
                                comment_data['date'] = date_published if date_published else 'Tarih yok'

                                if comment_data['comment']:
                                    self.comments.append(comment_data)
                                    reviews_found = True

            if reviews_found:
                print(f"JSON-LD'den {len(self.comments)} yorum çekildi")
            else:
                print("JSON-LD'de yorum bulunamadı, HTML'den çekilecek...")
                self._extract_comments_from_html()

        except Exception as e:
            print(f"Yorumlar çekilirken hata: {str(e)}")
            print("HTML'den yorumlar çekilmeye çalışılıyor...")
            self._extract_comments_from_html()

    def _extract_comments_from_html(self):
        """HTML'den yorumları çeker (fallback)"""
        try:
            # Tüm yorumları yüklemek için "Daha Fazla Göster" butonuna tıkla
            self._load_all_comments()

            # Çeşitli CSS selector'larını dene
            possible_selectors = [
                "div.comment-list div.rnr-com-card",
                "div[class*='review-card']",
                "div[class*='comment-card']",
                "div[class*='review']",
                "[class*='review-item']"
            ]

            comment_elements = []
            for selector in possible_selectors:
                comment_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if comment_elements:
                    print(f"'{selector}' ile {len(comment_elements)} yorum bulundu")
                    break

            if not comment_elements:
                print("HTML'de yorum bulunamadı")
                return

            # İlk 2 elementi atla (genellikle filtre/sıralama elementleri)
            comment_elements = comment_elements[2:] if len(comment_elements) > 2 else comment_elements

            for idx, comment_elem in enumerate(comment_elements, 1):
                # Maksimum yorum sayısına ulaşıldıysa dur
                if self.max_comments and len(self.comments) >= self.max_comments:
                    print(f"Maksimum yorum sayısına ({self.max_comments}) ulaşıldı")
                    break

                try:
                    comment_data = {}

                    # "Devamını oku" butonunu kontrol et ve tıkla
                    try:
                        # Önce XPath ile text içeriğine göre ara
                        try:
                            read_more_button = comment_elem.find_element(By.XPATH, ".//a[contains(text(), 'Devamını oku')] | .//button[contains(text(), 'Devamını oku')] | .//span[contains(text(), 'Devamını oku')]")
                        except:
                            # Yoksa class'a göre ara
                            read_more_button = comment_elem.find_element(By.CSS_SELECTOR, "a[class*='read-more'], button[class*='read-more'], [class*='show-more'], [class*='devamini-oku']")

                        if read_more_button and read_more_button.is_displayed():
                            self.driver.execute_script("arguments[0].click();", read_more_button)
                            time.sleep(0.5)
                            print(f"Yorum {idx} için 'Devamını oku' butonuna tıklandı")
                    except:
                        pass  # Buton yoksa devam et

                    # Kullanıcı adı - çeşitli selector'ları dene
                    user_selectors = [
                        "span[class*='rnr-com-tx']",
                        "span[class*='user']",
                        "div[class*='author']",
                        "[class*='reviewer-name']"
                    ]
                    for selector in user_selectors:
                        try:
                            user_name = comment_elem.find_element(By.CSS_SELECTOR, selector).text
                            if user_name:
                                comment_data['user'] = user_name
                                break
                        except:
                            continue
                    if 'user' not in comment_data:
                        comment_data['user'] = "Anonim"

                    # Yorum metni - çeşitli selector'ları dene
                    comment_selectors = [
                        "div.comment-text",
                        "div[class*='comment-text']",
                        "div[class*='review-text']",
                        "p[class*='comment']",
                        "div[class*='body']"
                    ]
                    for selector in comment_selectors:
                        try:
                            comment_text = comment_elem.find_element(By.CSS_SELECTOR, selector).text
                            if comment_text:
                                comment_data['comment'] = comment_text
                                break
                        except:
                            continue
                    if 'comment' not in comment_data:
                        comment_data['comment'] = ""

                    # Tarih
                    date_selectors = [
                        "span[class*='rnr-com-date']",
                        "span[class*='date']",
                        "time"
                    ]
                    for selector in date_selectors:
                        try:
                            date = comment_elem.find_element(By.CSS_SELECTOR, selector).text
                            if date:
                                comment_data['date'] = date
                                break
                        except:
                            continue
                    if 'date' not in comment_data:
                        comment_data['date'] = "Tarih yok"

                    if comment_data['comment']:  # Sadece yorum varsa ekle
                        self.comments.append(comment_data)
                        print(f"Yorum {idx} eklendi")

                except Exception as e:
                    print(f"Yorum {idx} çekilirken hata: {str(e)}")
                    continue

            print(f"HTML'den toplam {len(self.comments)} yorum çekildi")

        except Exception as e:
            print(f"HTML'den yorumlar çekilirken hata: {str(e)}")

    def _load_all_comments(self):
        """Tüm yorumları yüklemek için 'Daha Fazla' butonlarına tıklar"""
        max_clicks = 100  # Maksimum tıklama sayısı
        clicks = 0

        while clicks < max_clicks:
            try:
                # Sayfadaki mevcut yorum sayısını kontrol et
                if self.max_comments:
                    # Yorum elementlerini say
                    possible_selectors = [
                        "div.comment-list div.rnr-com-card",
                        "div[class*='review-card']",
                        "div[class*='comment-card']",
                    ]
                    current_comment_count = 0
                    for selector in possible_selectors:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            current_comment_count = len(elements) - 2  # İlk 2'yi çıkar (filtre elementleri)
                            break

                    # Yeterli yorum varsa dur
                    if current_comment_count >= self.max_comments:
                        print(f"Yeterli yorum yüklendi ({current_comment_count}), daha fazla yükleme yapılmayacak")
                        break

                # "Daha fazla yorum göster" butonunu bul
                load_more = self.driver.find_element(By.CSS_SELECTOR, "button[class*='load-more'], button[class*='show-more']")

                if load_more.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
                    time.sleep(1)
                    load_more.click()
                    time.sleep(2)
                    clicks += 1
                    print(f"Daha fazla yorum yüklendi (tıklama #{clicks})")
                else:
                    break
            except:
                # Buton bulunamazsa veya tıklanamazsa döngüden çık
                break

    def _extract_rating(self, rating_class):
        """Yıldız puanını class'tan çıkarır"""
        try:
            if 'full' in rating_class.lower():
                return "5"
            elif '4' in rating_class:
                return "4"
            elif '3' in rating_class:
                return "3"
            elif '2' in rating_class:
                return "2"
            elif '1' in rating_class:
                return "1"
            return "N/A"
        except:
            return "N/A"

    def export_to_word(self, filename="trendyol_yorumlar.docx"):
        """
        Yorumları Word dosyasına aktarır

        Args:
            filename (str): Çıktı dosya adı
        """
        if not self.comments:
            print("Henüz yorum çekilmedi!")
            return

        doc = Document()

        # Başlık
        title = doc.add_heading('Trendyol Ürün Yorumları', 0)
        title.alignment = 1  # Ortalanmış

        # Ürün bilgileri
        doc.add_heading('Ürün Bilgileri', level=1)
        for key, value in self.product_info.items():
            p = doc.add_paragraph()
            p.add_run(f"{key.capitalize()}: ").bold = True
            p.add_run(str(value))

        doc.add_paragraph()
        doc.add_heading(f'Toplam Yorum Sayısı: {len(self.comments)}', level=2)
        doc.add_paragraph()

        # Yorumlar
        doc.add_heading('Yorumlar', level=1)

        for idx, comment in enumerate(self.comments, 1):
            # Yorum başlığı
            doc.add_heading(f'Yorum #{idx}', level=2)

            # Kullanıcı bilgisi
            p = doc.add_paragraph()
            p.add_run('Kullanıcı: ').bold = True
            p.add_run(comment.get('user', 'Anonim'))

            # Tarih
            p = doc.add_paragraph()
            p.add_run('Tarih: ').bold = True
            p.add_run(comment.get('date', 'Bilinmiyor'))

            # Yorum metni
            p = doc.add_paragraph()
            p.add_run('Yorum: ').bold = True
            doc.add_paragraph(comment.get('comment', ''))

            # Ayırıcı
            doc.add_paragraph('_' * 80)

        doc.save(filename)
        print(f"Word dosyası oluşturuldu: {filename}")

    def export_to_pdf(self, filename="trendyol_yorumlar.pdf"):
        """
        Yorumları PDF dosyasına aktarır

        Args:
            filename (str): Çıktı dosya adı
        """
        if not self.comments:
            print("Henüz yorum çekilmedi!")
            return

        # PDF oluştur
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Özel stiller
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=black,
            spaceAfter=30,
            alignment=TA_LEFT
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=black,
            spaceAfter=12,
            spaceBefore=12
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_LEFT
        )

        # Başlık
        story.append(Paragraph("Trendyol Ürün Yorumları", title_style))
        story.append(Spacer(1, 0.2*inch))

        # Ürün bilgileri
        story.append(Paragraph("Ürün Bilgileri", heading_style))
        for key, value in self.product_info.items():
            text = f"<b>{key.capitalize()}:</b> {value}"
            story.append(Paragraph(text, normal_style))

        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"<b>Toplam Yorum Sayısı:</b> {len(self.comments)}", normal_style))
        story.append(Spacer(1, 0.3*inch))

        # Yorumlar
        story.append(Paragraph("Yorumlar", heading_style))
        story.append(Spacer(1, 0.2*inch))

        for idx, comment in enumerate(self.comments, 1):
            # Yorum başlığı
            story.append(Paragraph(f"<b>Yorum #{idx}</b>", heading_style))

            # Kullanıcı
            text = f"<b>Kullanıcı:</b> {comment.get('user', 'Anonim')}"
            story.append(Paragraph(text, normal_style))

            # Tarih
            text = f"<b>Tarih:</b> {comment.get('date', 'Bilinmiyor')}"
            story.append(Paragraph(text, normal_style))

            # Yorum metni
            comment_text = comment.get('comment', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            text = f"<b>Yorum:</b> {comment_text}"
            story.append(Paragraph(text, normal_style))

            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("_" * 100, normal_style))
            story.append(Spacer(1, 0.2*inch))

        # PDF'i oluştur
        doc.build(story)
        print(f"PDF dosyası oluşturuldu: {filename}")


def main():
    """Ana fonksiyon - örnek kullanım"""
    # Trendyol ürün URL'si (örnek)
    url = input("Trendyol ürün URL'sini girin: ")

    # Maksimum yorum sayısı
    max_comments_input = input("Maksimum kaç yorum çekmek istersiniz? (Tümü için Enter'a basın): ").strip()
    max_comments = int(max_comments_input) if max_comments_input else None

    # Scraper başlat
    scraper = TrendyolScraper(headless=False, max_comments=max_comments)  # headless=True yaparak arka planda çalıştırabilirsiniz

    try:
        # Yorumları çek
        result = scraper.scrape_product(url)

        print(f"\n{'='*50}")
        print(f"Ürün: {result['product_info'].get('name', 'Bilinmiyor')}")
        print(f"Toplam {result['total_comments']} yorum çekildi")
        print(f"{'='*50}\n")

        # Dosyaya kaydet (sadece Word formatı)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scraper.export_to_word(f"trendyol_yorumlar_{timestamp}.docx")

        print("\nİşlem tamamlandı!")

    except Exception as e:
        print(f"Hata: {str(e)}")


if __name__ == "__main__":
    main()
