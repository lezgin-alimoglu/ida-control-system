FROM ubuntu:22.04

# Sistem güncelle ve temel paketleri kur
RUN apt update && apt install -y \
    python3 python3-pip python3-dev \
    python3-pygame \
    libxml2-dev libxslt1-dev zlib1g-dev \
    libudev-dev libusb-1.0-0-dev \
    git sudo curl && \
    apt clean

# Python kütüphaneleri
RUN pip3 install pymavlink mavproxy numpy

# Çalışma dizini
WORKDIR /app

# Kodları kopyala
COPY . .

CMD ["python3", "main.py"]
