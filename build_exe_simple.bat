@echo off
title Trendyol Scraper - EXE Olusturucu
color 0B
echo.
echo ========================================
echo   TRENDYOL SCRAPER EXE OLUSTURUCU
echo ========================================
echo.
echo PyInstaller yukleniyor...
pip install pyinstaller
echo.
echo EXE dosyasi olusturuluyor...
echo Bu islem birkac dakika surebilir...
echo.
pyinstaller --onefile --windowed --name=TrendyolScraper --hidden-import=selenium --hidden-import=docx --hidden-import=reportlab --hidden-import=tkinter --collect-all=selenium --collect-all=reportlab gui_scraper.py
echo.
echo ========================================
echo   TAMAMLANDI!
echo ========================================
echo.
echo EXE dosyasi: dist\TrendyolScraper.exe
echo.
pause
