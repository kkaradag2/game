# Stratejik Tahta Oyunu

Pygame kullanılarak geliştirilmiş, insan ve yapay zeka oyuncusunun yer aldığı bir stratejik tahta oyunu. Yapay zeka, Min-Max algoritması, Alpha-Beta budaması ve stratejik değerlendirmelerle akıllı hamleler yapar.

## 🎮 Özellikler

- **7x7 Izgara Tabanlı Oyun:** Sıra tabanlı strateji oyunu.
- **İnsan vs Yapay Zeka:** Akıllı bir yapay zekaya veya başka bir insana karşı oynayın.
- **Min-Max Algoritması:** Alpha-Beta budaması ile optimize edilmiş karar mekanizması.
- **Gelişmiş Stratejiler:**
  - **Taş Konumlandırma:** Merkezdeki ve stratejik pozisyonlar önceliklidir.
  - **Saldırı ve Savunma:** Hem saldırgan hem de savunma senaryolarını dikkate alır.
- **Kazanan Tespiti:** Bir oyuncunun taşı kalmadığında kazanan ekrana gösterilir.
- **Görsel Geribildirim:** 
  - Yapay zeka hesaplama yaparken ekranda "Hesaplanıyor..." mesajı gösterilir.

![Oyun görünümü](/assets/images/game_welcome.png)

## 🚀 Kurulum

### 1. Gereksinimler
- Python 3.8 veya üzeri
- Pygame modülü (kurulumu aşağıda belirtilmiştir)

### 2. Depoyu Klonlayın
```bash
git clone https://github.com/kkaradag2/game.git
cd game
```

## Oyun Kuralları

### 3.1 Genel Kurallar
- Tahta bir başlangıç değeri ile açılır.
- Tahta 7x7 büyüklüğündedir.
- **AI oyuncu**: 4 adet mavi üçgen taşlara sahiptir.
- **İnsan oyuncu**: 4 adet kırmızı çember taşlara sahiptir.
- Rakibin iki taşı arasında kalan taşlar tahtadan silinir.  
  **Örnek:** `Çember-Üçgen-Çember -> Üçgen silinir`.
- Bir duvarla ve rakip taşla sıkıştırılan taş silinir.
- Bir oyuncunun birden fazla taşı varsa, farklı taşlar olmak üzere iki hamle yapar.
- Oyun, maksimum **50 hamle** ile sınırlıdır.

### 3.2 Taşları Hareket Ettirme Kuralları
- Taşlar **dikey** ve **yatay** olarak hareket ettirilebilir.  
  Çapraz hareketlere izin verilmez.
- Bir oyuncuda birden fazla taş varsa, oynattığı taşın dışında başka bir taşı da hareket ettirmelidir.  
  **Not:** Birden fazla taşı olan oyuncu iki hamle yapar.
- Oyuncunun yalnızca bir taşı varsa, sadece bir taş hareket ettirebilir.

### 3.3 Rakip Taşları Yeme Kuralları
- Bir ya da birden fazla taş, duvar ile rakip taş arasında bırakılırsa, arada kalan taşlar yenilir.
- Yenilen taşlar tahtadan kaldırılır ve rakip oyuncunun skoru, yenilen taş kadar azalır.
- Taşları yiyen oyuncunun skoru, yenilen taş kadar artırılır.

### 3.4 Oyunun Bitirilme Kuralları
- Oyuncunun taşları varken rakibin taşları tükenirse: **Oyuncu kazanır.**
- Oyuncunun taşları tükenirken rakibin taşları varsa: **Oyuncu kaybeder.**

### 3.5 Toplamda 50 Hamle Sonrasında
- Her iki oyuncunun taş sayısı eşitse: **Beraberlik.**
- Oyuncunun taş sayısı daha fazlaysa: **Oyuncu kazanır.**
- Aksi durumda: **Oyuncu kaybeder.**
