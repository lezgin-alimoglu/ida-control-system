#!/bin/bash

# =========================
# Python Sanal Ortam Kurulumu
# =========================
echo "Python sanal ortamı oluşturuluyor..."
python3 -m venv .venv
source .venv/bin/activate

# =========================
# Sistem Bağımlılıkları (Linux için)
# =========================
echo "Sistem bağımlılıkları yükleniyor (sudo gerektirir)..."
sudo apt-get update
sudo apt-get install -y libdbus-1-dev libdbus-glib-1-dev python3-dbus dbus

# NVIDIA kullanıyorsan, sürücüler güncel mi kontrol et:
# sudo apt-get install --reinstall nvidia-driver-XXX

# =========================
# Python Paketleri
# =========================
echo "Python bağımlılıkları yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

# Kivy Garden MapView ek paketi
echo "Kivy Garden MapView yükleniyor..."
python -m pip install kivy-garden
python -m pip install kivy_garden.mapview

# Alternatif: Eğer garden komutu çalışıyorsa
# python -m kivy_garden install mapview

# =========================
# D-Bus Sorunları için Ekstra
# =========================
echo "D-Bus servisi çalışıyor mu kontrol ediliyor..."
systemctl status dbus || echo "D-Bus servisi çalışmıyor! Lütfen kontrol edin."

# =========================
# Kullanıcıya Ekstra Bilgi
# =========================
echo ""
echo "Kurulum tamamlandı!"
echo "Eğer NVIDIA veya D-Bus ile ilgili hata alırsanız:"
echo "- Sudo ile çalıştırmayın."
echo "- Sistemi yeniden başlatmayı deneyin."
echo "- Hala hata alırsanız, tam hata mesajını paylaşın."
echo ""
echo "Kivy GUI başlatmak için:"
echo "python3 gui/waypoint_selector_kivy.py"
echo ""
echo "Ana programı başlatmak için:"
echo "python3 main.py"



