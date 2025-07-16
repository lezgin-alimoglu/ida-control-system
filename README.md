# IDA Control System

## Açıklama
Bu proje, insansız deniz aracı (IDA) için yer kontrol istasyonu ve otomatik/mekanik kontrol sistemlerini içerir. MAVLink protokolü ile haberleşir, joystick ile manuel kontrol ve görev planlama (waypoint) desteği sunar.

## Kurulum

1. **Python 3.7+** yüklü olmalı.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Linux'ta joystick desteği için ek paketler gerekebilir:
   ```bash
   sudo apt-get install joystick python3-tk
   ```
4. Raspberry Pi kullanıyorsanız, GPIO desteği için:
   ```bash
   sudo apt-get install python3-rpi.gpio
   ```

## Kullanım

```bash
python main.py
```

- **1 - Manual Control:** Joystick ile aracı manuel kontrol edin.
- **2 - Mission Planner (GUI):** Görev noktalarını (waypoint) girin ve aracı otonom olarak yönlendirin.
- **0 - Exit:** Programı kapatır.

## Bağımlılıklar
- pymavlink
- pygame
- folium
- pyserial
- tkinter (bazı sistemlerde python3-tk olarak kurulur)
- RPi.GPIO (sadece Raspberry Pi için)

## Donanım Gereksinimleri
- MAVLink destekli araç (ör. ArduPilot tabanlı)
- USB veya UDP üzerinden bağlantı
- Joystick (manuel kontrol için)
- Raspberry Pi (isteğe bağlı, GPIO için)

## Dikkat Edilmesi Gerekenler
- MAVLink bağlantı ayarlarını `config.py` dosyasından düzenleyin.
- Kodun bazı bölümleri donanım bağımlıdır, farklı platformlarda çalışmayabilir.
- Hatalar ve öneriler için lütfen issue açın.
