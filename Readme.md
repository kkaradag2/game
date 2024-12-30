# Stratejik Tahta Oyunu

Pygame kullanılarak geliştirilmiş, insan ve yapay zeka oyuncusunun yer aldığı bir stratejik tahta oyunu. Yapay zeka, Min-Max algoritması, Alpha-Beta budaması ve stratejik değerlendirmelerle akıllı hamleler yapar.


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

![Oyun görünümü](/assets/images/game_welcome.png)

## 🚀 Kurulum

## 1. **Gereksinimler:**
   - Python 3.8 veya üzeri
   - Pygame modülü (kurulumu aşağıda belirtilmiştir)

## 2. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/kkaradag2/game.git
   cd game

## 3. **Oyun Kuralları:**
    - Tahta bir başlangıç değeri ile açılır.
    - Tahta 7x7 büyüklüğündedir
    - AI oyuncu 4 adet Mavi üçgen taşlara sahiptir
    - insan oyuncu 4 ader Kırmızı çember taşlara sahiptir.
    - rakibin iki taşı rasında kalan taşlar tahtadan silinir. (Ör: Çember-Üçgen-Çember -> Üçgen silinir)
    - Bir duvarla ve rakip taşla sıkıştırılan taş silinir.
    - Bir oyuncunun birden fazla taşı varsa farklı taşlar olmak  üzere iki hamle yapar
    - Max 50 hamle ile oyun sınırlıdır.

## 3.1. Taşları Haraket Ettirme Kuralları

    - Taşlar dikey ve yatay olarak hareket ettirilebilir. Çapraz haraketlere izin verilmeyecektir.
    - Bir oyuncuda birden fazla taş varsa oynatığı taşın dışında bir başka taşıda hareket ettirmelidir. Yani birden fazla taşı olan oyuncu iki el oynar.
    - Oyuncunun sadece bir taşı varsa sadece bir taş hareket ettirebilir.

## 3.2 Rakip Taşları Yeme Kuralları

    - Bir yada birden fazla taş duvar ile rakip oyuncu arasında bırakılırsa, arada kalan rakip taşları yenilir. Yanı tahtadan kaldırılarak oyuncusunun skoru yenilen taş kadar azaltılır. Taşları yiyen oyuncunun da skoru yenilen taş kadar artırılır.

 ## 3.3 Oyunun Bitirilme Kuralları

    - Oyuncunun taşları varken, rakip oyuncunun hiç taşı yoksa: Oyuncu kazanır.
    - Oyuncunun hiç taşı yokken, rakip oyuncunun taşları varsa:Oyuncu kaybeder.

## 3.4 **Toplamda 50 hamle sonrasında:**

    - Eğer her iki oyuncunun taş sayısı eşitse: Beraberlik.
    - Eğer oyuncunun taş sayısı daha fazlaysa: Oyuncu kazanır.
    - Aksi halde: Oyuncu kaybeder.