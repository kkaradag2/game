# Stratejik Tahta Oyunu

Pygame kullanılarak geliştirilmiş, insan ve yapay zeka oyuncusunun yer aldığı bir stratejik tahta oyunu. Yapay zeka, Min-Max algoritması, Alpha-Beta budaması ve stratejik değerlendirmelerle akıllı hamleler yapar.

---

## 🎮 Özellikler

- **7x7 Izgara Tabanlı Oyun:** Sıra tabanlı strateji oyunu.
- **İnsan vs Yapay Zeka:** Akıllı bir yapay zekaya veya başka bir insana karşı oynayın.
- **Min-Max Algoritmasıyla Yapay Zeka:** Alpha-Beta budaması ile optimize edilmiş karar mekanizması.
- **Gelişmiş Stratejiler:**
  - **Taş Konumlandırma:** Merkezdeki ve stratejik pozisyonlar önceliklidir.
  - **Saldırı ve Savunma Değerlendirmesi:** Hem saldırgan hem de savunma senaryolarını dikkate alır.
- **Kazanan Tespiti:** Bir oyuncunun taşı kalmadığında kazanan ekrana gösterilir.
- **Görsel Geribildirim:**
  - Yapay zeka hesaplama yaparken ekranda "Hesaplanıyor..." mesajı gösterilir.

---

## 🚀 Kurulum

1. **Gereksinimler:**
   - Python 3.8 veya üzeri
   - Pygame modülü (kurulumu aşağıda belirtilmiştir)

2. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/kkaradag2/game.git
   cd game

3. **Oyun Kuralları:**
    - Tahta bir başlangıç değeri ile açılır.
    - AI oyuncu 4 adet Mavi üçgen taşlara sahiptir
    - insan oyuncu 4 ader Kırmızı çember taşlara sahiptir.
    - rakibin iki taşı rasında kalan taşlar tahtadan silinir. (Ör: Çember-Üçgen-Çember -> Üçgen silinir)
    - Bir duvarla ve rakip taşla sıkıştırılan taş silinir.
    - Bir oyuncunun birden fazla taşı varsa farklı taşlar olmak  üzere iki hamle yapar
    - Max 50 hamle ile oyun sınırlıdır.