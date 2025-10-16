import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
from io import StringIO
import threading
from datetime import datetime
from trendyol_scraper import TrendyolScraper


class LogRedirector:
    """Terminal çıktılarını GUI'ye yönlendirir"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = StringIO()

    def write(self, string):
        self.text_widget.config(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state='disabled')
        self.text_widget.update_idletasks()

    def flush(self):
        pass


class TrendyolScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trendyol Scraper - Mavi Tema")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)

        # Mavi renk paleti
        self.colors = {
            'primary': '#1E3A8A',      # Koyu mavi
            'secondary': '#3B82F6',    # Orta mavi
            'accent': '#60A5FA',       # Açık mavi
            'light': '#DBEAFE',        # Çok açık mavi
            'background': '#F8FAFC',   # Beyaz-gri
            'text': '#1E293B',         # Koyu gri
            'success': '#10B981',      # Yeşil
            'warning': '#F59E0B',      # Turuncu
            'error': '#EF4444'         # Kırmızı
        }

        self.scraper = None
        self.result = None
        self.is_scraping = False

        self.setup_ui()
        self.redirect_output()

    def setup_ui(self):
        """Ana UI bileşenlerini oluşturur"""
        # Ana container
        self.root.configure(bg=self.colors['background'])

        # Başlık
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🛍️ Trendyol Scraper",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(pady=20)

        # Ana içerik alanı
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Sol panel - Kontroller
        left_panel = tk.Frame(main_frame, bg='white', relief='flat', borderwidth=0)
        left_panel.pack(side='left', fill='both', padx=(0, 10), pady=0)

        # Kontrol paneli içeriği
        self.create_control_panel(left_panel)

        # Sağ panel - Log alanı
        right_panel = tk.Frame(main_frame, bg='white', relief='flat', borderwidth=0)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=0)

        # Log alanı içeriği
        self.create_log_panel(right_panel)

    def create_control_panel(self, parent):
        """Sol taraftaki kontrol panelini oluşturur"""
        # Padding frame
        control_frame = tk.Frame(parent, bg='white')
        control_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # URL girişi
        url_label = tk.Label(
            control_frame,
            text="Ürün URL:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        url_label.pack(anchor='w', pady=(0, 5))

        self.url_entry = tk.Entry(
            control_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            width=40
        )
        self.url_entry.pack(fill='x', pady=(0, 20), ipady=8)
        self.url_entry.config(highlightthickness=2, highlightcolor=self.colors['secondary'])

        # Mod seçimi
        mode_label = tk.Label(
            control_frame,
            text="Scraping Modu:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        mode_label.pack(anchor='w', pady=(0, 10))

        self.scrape_mode = tk.StringVar(value='comments')

        mode_frame = tk.Frame(control_frame, bg='white')
        mode_frame.pack(fill='x', pady=(0, 20))

        rb1 = tk.Radiobutton(
            mode_frame,
            text="📝 Ürün Yorumları",
            variable=self.scrape_mode,
            value='comments',
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text'],
            activebackground='white',
            selectcolor=self.colors['light']
        )
        rb1.pack(anchor='w', pady=5)

        rb2 = tk.Radiobutton(
            mode_frame,
            text="⭐ Mağaza Değerlendirmeleri",
            variable=self.scrape_mode,
            value='reviews',
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text'],
            activebackground='white',
            selectcolor=self.colors['light']
        )
        rb2.pack(anchor='w', pady=5)

        # Maksimum yorum sayısı
        max_label = tk.Label(
            control_frame,
            text="Maksimum Sayı (opsiyonel):",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        )
        max_label.pack(anchor='w', pady=(0, 5))

        self.max_comments_entry = tk.Entry(
            control_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            width=40
        )
        self.max_comments_entry.pack(fill='x', pady=(0, 20), ipady=8)
        self.max_comments_entry.config(highlightthickness=2, highlightcolor=self.colors['secondary'])
        self.max_comments_entry.insert(0, "Boş bırakırsanız tümünü çeker")
        self.max_comments_entry.config(fg='gray')
        self.max_comments_entry.bind('<FocusIn>', self.on_max_comments_focus_in)
        self.max_comments_entry.bind('<FocusOut>', self.on_max_comments_focus_out)

        # Headless mode checkbox
        self.headless_var = tk.BooleanVar(value=False)
        headless_cb = tk.Checkbutton(
            control_frame,
            text="🔇 Arka plan modu (tarayıcıyı gizle)",
            variable=self.headless_var,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text'],
            activebackground='white',
            selectcolor=self.colors['light']
        )
        headless_cb.pack(anchor='w', pady=(0, 30))

        # Başlat butonu
        self.start_button = tk.Button(
            control_frame,
            text="🚀 Scraping Başlat",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            activebackground=self.colors['primary'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.start_scraping
        )
        self.start_button.pack(fill='x', pady=(0, 10), ipady=12)

        # Word Export butonu
        self.word_button = tk.Button(
            control_frame,
            text="📄 Word Export",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground='#059669',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            state='disabled',
            command=self.export_word
        )
        self.word_button.pack(fill='x', pady=(10, 0), ipady=12)

        # Temizle butonu
        clear_button = tk.Button(
            control_frame,
            text="🗑️ Logları Temizle",
            font=('Segoe UI', 9),
            bg=self.colors['warning'],
            fg='white',
            activebackground='#D97706',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            command=self.clear_logs
        )
        clear_button.pack(fill='x', pady=(20, 0), ipady=8)

    def create_log_panel(self, parent):
        """Sağ taraftaki log panelini oluşturur"""
        # Padding frame
        log_frame = tk.Frame(parent, bg='white')
        log_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Log başlığı
        log_header = tk.Frame(log_frame, bg=self.colors['light'], height=40)
        log_header.pack(fill='x', pady=(0, 10))
        log_header.pack_propagate(False)

        log_title = tk.Label(
            log_header,
            text="📊 İşlem Logları",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['primary']
        )
        log_title.pack(side='left', padx=15, pady=10)

        # Status label
        self.status_label = tk.Label(
            log_header,
            text="● Hazır",
            font=('Segoe UI', 10),
            bg=self.colors['light'],
            fg=self.colors['success']
        )
        self.status_label.pack(side='right', padx=15, pady=10)

        # Log text alanı
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 9),
            bg='#F1F5F9',
            fg=self.colors['text'],
            relief='flat',
            borderwidth=0,
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True)

        # Log text tag'leri (renklendirme için)
        self.log_text.tag_config('success', foreground=self.colors['success'], font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('error', foreground=self.colors['error'], font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('warning', foreground=self.colors['warning'], font=('Consolas', 9, 'bold'))
        self.log_text.tag_config('info', foreground=self.colors['secondary'], font=('Consolas', 9, 'bold'))

    def on_max_comments_focus_in(self, event):
        """Placeholder text'i temizle"""
        if self.max_comments_entry.get() == "Boş bırakırsanız tümünü çeker":
            self.max_comments_entry.delete(0, tk.END)
            self.max_comments_entry.config(fg=self.colors['text'])

    def on_max_comments_focus_out(self, event):
        """Boşsa placeholder text'i geri koy"""
        if not self.max_comments_entry.get():
            self.max_comments_entry.insert(0, "Boş bırakırsanız tümünü çeker")
            self.max_comments_entry.config(fg='gray')

    def redirect_output(self):
        """Terminal çıktılarını log paneline yönlendir"""
        sys.stdout = LogRedirector(self.log_text)
        sys.stderr = LogRedirector(self.log_text)

    def log(self, message, level='info'):
        """Log mesajı ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.log_text.config(state='normal')

        if level == 'success':
            self.log_text.insert(tk.END, formatted_message, 'success')
        elif level == 'error':
            self.log_text.insert(tk.END, formatted_message, 'error')
        elif level == 'warning':
            self.log_text.insert(tk.END, formatted_message, 'warning')
        else:
            self.log_text.insert(tk.END, formatted_message, 'info')

        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def update_status(self, text, color):
        """Status label'ı güncelle"""
        self.status_label.config(text=f"● {text}", fg=color)

    def clear_logs(self):
        """Log alanını temizle"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.log("Loglar temizlendi", 'info')

    def validate_inputs(self):
        """Girdileri doğrula"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Hata", "Lütfen bir URL girin!")
            return False

        if not url.startswith('https://www.trendyol.com/'):
            messagebox.showerror("Hata", "Geçerli bir Trendyol URL'si girin!")
            return False

        max_comments_text = self.max_comments_entry.get().strip()
        if max_comments_text and max_comments_text != "Boş bırakırsanız tümünü çeker":
            try:
                max_val = int(max_comments_text)
                if max_val <= 0:
                    messagebox.showerror("Hata", "Maksimum sayı pozitif bir sayı olmalı!")
                    return False
            except ValueError:
                messagebox.showerror("Hata", "Maksimum sayı geçerli bir sayı olmalı!")
                return False

        return True

    def start_scraping(self):
        """Scraping işlemini başlat"""
        if self.is_scraping:
            messagebox.showwarning("Uyarı", "Bir scraping işlemi zaten devam ediyor!")
            return

        if not self.validate_inputs():
            return

        # Thread içinde çalıştır
        thread = threading.Thread(target=self.run_scraping)
        thread.daemon = True
        thread.start()

    def run_scraping(self):
        """Scraping işlemini çalıştır (thread içinde)"""
        try:
            self.is_scraping = True
            self.update_status("Çalışıyor...", self.colors['warning'])

            # Butonları devre dışı bırak
            self.start_button.config(state='disabled', bg='gray')
            self.word_button.config(state='disabled', bg='gray')

            # Parametreleri al
            url = self.url_entry.get().strip()
            scrape_mode = self.scrape_mode.get()
            headless = self.headless_var.get()

            max_comments_text = self.max_comments_entry.get().strip()
            max_comments = None
            if max_comments_text and max_comments_text != "Boş bırakırsanız tümünü çeker":
                max_comments = int(max_comments_text)

            # Scraper oluştur
            self.log("="*60, 'info')
            self.log(f"🚀 Scraping başlatılıyor...", 'info')
            self.log(f"URL: {url}", 'info')
            self.log(f"Mod: {scrape_mode}", 'info')
            self.log(f"Headless: {headless}", 'info')
            self.log(f"Maksimum: {max_comments if max_comments else 'Tümü'}", 'info')
            self.log("="*60, 'info')

            self.scraper = TrendyolScraper(headless=headless, max_comments=max_comments)

            # Scraping yap
            self.result = self.scraper.scrape_product(url, scrape_mode=scrape_mode)

            # Başarılı
            self.log("="*60, 'success')
            self.log(f"✓ İşlem tamamlandı!", 'success')

            if scrape_mode == 'reviews':
                self.log(f"✓ Toplam {self.result['total_reviews']} değerlendirme çekildi", 'success')
            else:
                self.log(f"✓ Toplam {self.result['total_comments']} yorum çekildi", 'success')

            self.log(f"✓ Ürün: {self.result['product_info'].get('name', 'Bilinmiyor')}", 'success')
            self.log("="*60, 'success')

            # Export butonunu aktif et
            self.word_button.config(state='normal', bg=self.colors['success'])

            self.update_status("Tamamlandı", self.colors['success'])

        except Exception as e:
            self.log(f"✗ HATA: {str(e)}", 'error')
            self.update_status("Hata!", self.colors['error'])
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{str(e)}")

        finally:
            self.is_scraping = False
            self.start_button.config(state='normal', bg=self.colors['secondary'])

    def export_word(self):
        """Word export"""
        if not self.scraper:
            messagebox.showerror("Hata", "Önce scraping yapmalısınız!")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode = self.result['scrape_mode']
            filename = f"trendyol_{mode}_{timestamp}.docx"

            self.log(f"📄 Word dosyası oluşturuluyor: {filename}", 'info')
            self.scraper.export_to_word(filename)
            self.log(f"✓ Word dosyası oluşturuldu: {filename}", 'success')

            messagebox.showinfo("Başarılı", f"Word dosyası oluşturuldu:\n{filename}")

        except Exception as e:
            self.log(f"✗ Word export hatası: {str(e)}", 'error')
            messagebox.showerror("Hata", f"Word export hatası:\n{str(e)}")


def main():
    root = tk.Tk()
    app = TrendyolScraperGUI(root)

    # Başlangıç mesajı
    app.log("="*60, 'info')
    app.log("🎨 Trendyol Scraper GUI - Mavi Tema", 'info')
    app.log("="*60, 'info')
    app.log("✓ Uygulama hazır. Lütfen URL girin ve scraping'i başlatın.", 'success')
    app.log("", 'info')

    root.mainloop()


if __name__ == "__main__":
    main()
