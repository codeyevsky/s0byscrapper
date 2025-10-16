"""
Trendyol Scraper GUI'yi standalone .exe dosyasına dönüştürür
Python olmayan bilgisayarlarda çalışır
"""

import os
import sys
import subprocess

def build_exe():
    print("="*60)
    print("TRENDYOL SCRAPER - EXE OLUŞTURUCU")
    print("="*60)
    print()

    # PyInstaller kontrolü
    try:
        import PyInstaller
        print("✓ PyInstaller yüklü")
    except ImportError:
        print("✗ PyInstaller yüklü değil. Yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller yüklendi")

    print()
    print("EXE dosyası oluşturuluyor...")
    print("Bu işlem birkaç dakika sürebilir...")
    print()

    # PyInstaller komutu
    command = [
        "pyinstaller",
        "--onefile",                    # Tek dosya
        "--windowed",                   # Console penceresi gösterme
        "--name=TrendyolScraper",       # Exe adı
        "--icon=NONE",                  # İkon (yoksa NONE)
        "--add-data=trendyol_scraper.py;.",  # Ana scraper'ı dahil et
        "--hidden-import=selenium",
        "--hidden-import=selenium.webdriver",
        "--hidden-import=selenium.webdriver.chrome",
        "--hidden-import=selenium.webdriver.common.by",
        "--hidden-import=docx",
        "--hidden-import=reportlab",
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--collect-all=selenium",
        "--collect-all=reportlab",
        "gui_scraper.py"
    ]

    try:
        subprocess.check_call(command)
        print()
        print("="*60)
        print("✓ BAŞARILI!")
        print("="*60)
        print()
        print("EXE dosyası oluşturuldu:")
        print("📁 Konum: dist/TrendyolScraper.exe")
        print()
        print("Bu dosyayı istediğiniz bilgisayara kopyalayabilirsiniz!")
        print("Python yüklü olmasa bile çalışacak!")
        print()
        print("⚠ DİKKAT:")
        print("- Chrome tarayıcı hedef bilgisayarda olmalı")
        print("- ChromeDriver otomatik olarak yüklenecek")
        print()

    except Exception as e:
        print()
        print("="*60)
        print("✗ HATA!")
        print("="*60)
        print(f"Hata: {str(e)}")
        print()
        print("Manuel olarak şunu deneyin:")
        print("pip install pyinstaller")
        print("pyinstaller --onefile --windowed gui_scraper.py")

if __name__ == "__main__":
    build_exe()
    input("\nKapatmak için Enter'a basın...")
