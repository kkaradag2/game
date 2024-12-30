"""
###############################################################################
# 7x7 Stratejik Tahta Oyunu
# Author: Kemal Karadağ
# GitHub: https://github.com/kkaradag2/game
#
# Açıklama:
# Bu proje, Pygame kullanılarak geliştirilmiş bir stratejik tahta oyunudur. 
# Yapay zeka oyuncusu, Min-Max algoritması ve stratejik değerlendirmelerle
# insan oyuncuya karşı mücadele eder.
#
# Özellikler:
# - 7x7 ızgara tabanlı strateji oyunu
# - Min-Max algoritması ile akıllı yapay zeka
# - Saldırı ve savunma değerlendirmesi
# - Oyuncular için görsel geribildirim
#
###############################################################################
"""


import pygame
import random

WIDTH, HEIGHT = 700, 700
GRID_SIZE = 7
CELL_SIZE = WIDTH // GRID_SIZE

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pygame başlatma
pygame.init()

# Oyun ekranı
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Min-Max Board Game")

# Oyuncu taşları
P1_SYMBOL = "triangle"
P2_SYMBOL = "circle"
PLAYER_1 = {"symbol": P1_SYMBOL, "positions": [(0, 0), (0, 2), (6, 4), (6, 6)]}
PLAYER_2 = {"symbol": P2_SYMBOL, "positions": [(6, 0), (6, 2), (0, 4), (0, 6)]}

# Oyun değişkenleri
current_player = 1
turn_count = 0
max_turns = 50
selected_piece = None
moved_pieces = []  # Bir turda hareket ettirilen taşları takip eder
moves_remaining = 0  # Dinamik olarak belirlenecek
winner = None  # Kazananı takip etmek için global değişken

# Duvar pozisyonları
TOP_WALL = [(x, 0) for x in range(GRID_SIZE)]
BOTTOM_WALL = [(x, GRID_SIZE - 1) for x in range(GRID_SIZE)]
LEFT_WALL = [(0, y) for y in range(GRID_SIZE)]
RIGHT_WALL = [(GRID_SIZE - 1, y) for y in range(GRID_SIZE)]
ALL_WALLS = set(TOP_WALL + BOTTOM_WALL + LEFT_WALL + RIGHT_WALL)

def draw_board():
    """Oyun tahtasını çizer."""
    screen.fill(WHITE)
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_pieces():
    """Oyuncu taşlarını çizer."""
    for pos in PLAYER_1["positions"]:
        pygame.draw.polygon(screen, RED, [
            (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + 10),
            (pos[0] * CELL_SIZE + 10, pos[1] * CELL_SIZE + CELL_SIZE - 10),
            (pos[0] * CELL_SIZE + CELL_SIZE - 10, pos[1] * CELL_SIZE + CELL_SIZE - 10)
        ])
    for pos in PLAYER_2["positions"]:
        pygame.draw.circle(screen, BLUE, 
                           (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), 
                           CELL_SIZE // 3)

def evaluate_game():
    """Oyun durumunu ekrana yazar."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"P1: {len(PLAYER_1['positions'])} pieces, P2: {len(PLAYER_2['positions'])} pieces, Turns: {max_turns - turn_count}, Current: {'P1' if current_player == 1 else 'P2'}, Moves left: {moves_remaining}", True, BLACK)
    screen.blit(text, (10, 10))


# taşların koruma (savunma) ve saldırı (rakip taşları tehdit etme) durumlarını değerlendirme
# Bu özellik, taşların hem korunmasını hem de stratejik hamleler için rakibin taşlarını hedef almasını sağlar.
# Koruma, bir taşın kendi takım arkadaşları tarafından çevrili olma durumudur. Eğer bir taş, kendi takımından 
# bir veya daha fazla taş tarafından destekleniyorsa, bu durum bir avantajdır
# Saldırı, bir taşın rakip taşlara yakın olması durumudur. Eğer bir taş, rakip taşları tehdit edebilecek bir 
# konumdaysa, bu durum stratejik bir avantajdır
# Score=Player 1 Piece Count−Player 2 Piece Count+Center Bonus+Protection Bonus+Attack Bonus
def evaluate_state(state):
    """Durumu değerlendirir ve bir puan döndürür."""
    center = (GRID_SIZE // 2, GRID_SIZE // 2)  # 7x7 için merkez (3, 3)

    def calculate_center_bonus(positions):
        """Taşların merkeze yakınlığına göre bonus puan hesaplar."""
        bonus = 0
        for pos in positions:
            distance = abs(pos[0] - center[0]) + abs(pos[1] - center[1])
            bonus += (GRID_SIZE - distance)  # Daha yakın taşlar daha fazla puan alır
        return bonus

    def calculate_protection_bonus(player_positions):
        """Kendi takım arkadaşları tarafından korunan taşlar için bonus hesaplar."""
        bonus = 0
        for pos in player_positions:
            x, y = pos
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            # Komşulardan birinin aynı oyuncunun taşına ait olması koruma sağlar
            bonus += sum(1 for neighbor in neighbors if neighbor in player_positions)
        return bonus

    def calculate_attack_bonus(player_positions, opponent_positions):
        """Rakip taşlara yakın olan taşlar için bonus hesaplar."""
        bonus = 0
        for pos in player_positions:
            x, y = pos
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            # Komşulardan biri rakibin taşına aitse saldırı avantajı sağlanır
            bonus += sum(1 for neighbor in neighbors if neighbor in opponent_positions)
        return bonus

    # Player 1 değerlendirmesi
    player_1_positions = state["player_1"]
    player_1_center_bonus = calculate_center_bonus(player_1_positions)
    player_1_protection_bonus = calculate_protection_bonus(player_1_positions)
    player_1_attack_bonus = calculate_attack_bonus(player_1_positions, state["player_2"])

    # Player 2 değerlendirmesi
    player_2_positions = state["player_2"]
    player_2_center_bonus = calculate_center_bonus(player_2_positions)
    player_2_protection_bonus = calculate_protection_bonus(player_2_positions)
    player_2_attack_bonus = calculate_attack_bonus(player_2_positions, state["player_1"])

    # Toplam skor
    player_1_score = len(player_1_positions) + player_1_center_bonus + player_1_protection_bonus + player_1_attack_bonus
    player_2_score = len(player_2_positions) + player_2_center_bonus + player_2_protection_bonus + player_2_attack_bonus

    return player_1_score - player_2_score



def get_current_state():
    """Mevcut oyun durumunu döndür."""
    return {
        "player_1": PLAYER_1["positions"],
        "player_2": PLAYER_2["positions"]
    }


def minimax_alpha_beta(state, depth, alpha, beta, maximizing_player):
    """Minimax algoritmasının alpha-beta pruning ile uygulanması."""
    if depth == 0 or is_terminal_state(state):
        return evaluate_state(state)  # Mevcut durumun değerlendirme değeri

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(state, PLAYER_1):
            new_state = make_move(state, move, PLAYER_1)
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(state, PLAYER_2):
            new_state = make_move(state, move, PLAYER_2)
            eval = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return min_eval


def is_valid_move(x, y):
    """Hamlenin geçerli olup olmadığını kontrol eder."""
    if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
        print(f"Hedef kare ({x}, {y}) tahtanın dışında!")  # Debug
        return False
    if (x, y) in PLAYER_1["positions"] or (x, y) in PLAYER_2["positions"]:
        print(f"Hedef kare ({x}, {y}) dolu!")  # Debug
        return False
    print(f"Hedef kare ({x}, {y}) geçerli.")  # Debug
    return True

def get_random_move(pos):
    """Rastgele bir geçerli hareket döndürür."""
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(moves)
    for dx, dy in moves:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if is_valid_move(new_x, new_y):
            return (new_x, new_y)
    return pos  # Eğer hareket yoksa mevcut pozisyonu döndür

def start_turn():
    """Hamle sırası başladığında taş sayısına göre moves_remaining ayarla."""
    global moves_remaining, current_player, moved_pieces
    moved_pieces.clear()  # Yeni tur için temizle
    if current_player == 1:
        moves_remaining = min(2, len(PLAYER_1["positions"]))  # P1 için
    else:
        moves_remaining = min(2, len(PLAYER_2["positions"]))  # P2 için
    print(f"Sıra: {'P1' if current_player == 1 else 'P2'}, Kalan hamle: {moves_remaining}")  # Debug


def handle_player1_turn():
    best_move = None
    best_value = float('-inf')
    for move in get_possible_moves(current_state, PLAYER_1):
        new_state = make_move(current_state, move, PLAYER_1)
        move_value = minimax_alpha_beta(new_state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    # Hareketi uygula
    PLAYER_1["positions"].remove(best_move[0])
    PLAYER_1["positions"].append(best_move[1])
    print(f"Bilgisayar taşı hareket ettirildi: {best_move[1]}")

def get_possible_moves(state, player):
    """Verilen oyun durumunda geçerli hamleleri döndür."""
    possible_moves = []
    positions = state["player_1"] if player == PLAYER_1 else state["player_2"]

    for pos in positions:
        x, y = pos
        # Tüm olası hareketleri kontrol et (yukarı, aşağı, sola, sağa)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(new_x, new_y):
                possible_moves.append(((x, y), (new_x, new_y)))  # (eski_pozisyon, yeni_pozisyon)

    return possible_moves


def make_move(state, move, player):
    """Oyun durumunu bir hareketle günceller."""
    new_state = {
        "player_1": state["player_1"][:],
        "player_2": state["player_2"][:]
    }
    old_pos, new_pos = move
    if player == PLAYER_1:
        new_state["player_1"].remove(old_pos)
        new_state["player_1"].append(new_pos)
    else:
        new_state["player_2"].remove(old_pos)
        new_state["player_2"].append(new_pos)
    return new_state

def handle_player1_turn():
    """Player 1 (Bilgisayar) için Min-Max algoritması ile en iyi hamleyi hesaplar."""
    global current_player, moves_remaining, moved_pieces

    if moves_remaining == 0:
        return  # Eğer hamle hakkı kalmamışsa

    current_state = get_current_state()
    best_move = None
    best_value = float('-inf')  # Player 1 maximizasyon yapar

    draw_calculating_message()
    # Min-Max algoritması ile en iyi hamleyi bul
    for move in get_possible_moves(current_state, PLAYER_1):
        new_state = make_move(current_state, move, PLAYER_1)
        move_value = minimax_alpha_beta(
            state=new_state,
            depth=3,  # Derinliği artırabilirsiniz
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing_player=False  # Player 2'nin sırası simüle edilir
        )
        if move_value > best_value:
            best_value = move_value
            best_move = move

    if best_move:
        old_pos, new_pos = best_move
        PLAYER_1["positions"].remove(old_pos)
        PLAYER_1["positions"].append(new_pos)
        print(f"Bilgisayar taşı hareket ettirildi: {new_pos}")
        moved_pieces.append(old_pos)
        moves_remaining -= 1

        # Hamleden sonra kontrol yap
        check_for_eliminations()
        check_wall_captures()

    # Eğer hareketler tamamlandıysa sıra değiştir
    if moves_remaining == 0:
        current_player = 2

    """Bilgisayarın (P1) sırasını işler."""    
    start_turn()  # Mevcut tur için taş sayısını ayarla
    current_state = get_current_state()
    best_move = None

    while moves_remaining > 0:
        best_value = float('-inf')
        for move in get_possible_moves(current_state, PLAYER_1):
            new_state = make_move(current_state, move, PLAYER_1)
            move_value = minimax_alpha_beta(new_state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
            if move_value > best_value:
                best_value = move_value
                best_move = move

        if best_move:
            # Hareketi uygula
            old_pos, new_pos = best_move
            PLAYER_1["positions"].remove(old_pos)
            PLAYER_1["positions"].append(new_pos)
            moved_pieces.append(old_pos)  # Bu turda hareket ettirilen taşı kaydet
            print(f"Bilgisayar taşı hareket ettirildi: {new_pos}")
            moves_remaining -= 1

            # Hamleden sonra taş kontrolü
            check_for_eliminations()
            check_wall_captures()

    if moves_remaining == 0:
        current_player = 2  # Sıra insan oyuncuya geçer

def draw_calculating_message():
    """Ekranda 'Hesaplanıyor...' mesajını gösterir."""
    font = pygame.font.Font(None, 48)  # Yazı tipi ve boyut
    text_surface = font.render("Hesaplanıyor...", True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Ekranın ortasına yerleştir
    screen.blit(text_surface, text_rect)
    pygame.display.flip()  # Çizilenleri ekranda göster

def is_terminal_state(state):
    """Oyun durumunun terminal durumda olup olmadığını kontrol eder."""
    # Eğer herhangi bir oyuncunun taşı kalmamışsa terminal durumdur
    if not state["player_1"]:  # PLAYER_1'in taşları tükenmişse
        print("PLAYER 2 kazandı!")
        return True
    if not state["player_2"]:  # PLAYER_2'nin taşları tükenmişse
        print("PLAYER 1 kazandı!")
        return True
    # Eğer başka bir terminal durum kuralı varsa buraya ekleyin
    return False


def handle_player2_turn(event):
    """İnsanın (P2) sırasını işler."""
    global current_player, selected_piece, moves_remaining, moved_pieces

    if moves_remaining == 0:
        return  # Eğer hamle hakkı kalmamışsa

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

        # Eğer bir taş seçilmemişse, taş seçimi yap
        if selected_piece is None:
            for i, pos in enumerate(PLAYER_2["positions"]):
                if pos == (grid_x, grid_y):
                    if i in moved_pieces:
                        print(f"Taş ({grid_x}, {grid_y}) zaten bu turda hareket ettirildi!")  # Debug
                        return
                    selected_piece = i
                    print(f"Seçilen taş: {pos}")  # Debug
                    return
            print(f"Hiçbir taş seçilmedi. Belirtilen karede taş yok: ({grid_x}, {grid_y})")  # Debug

        # Eğer bir taş seçilmişse, hedef kareye taşımayı dene
        else:
            print(f"Hareket denemesi: {PLAYER_2['positions'][selected_piece]} -> ({grid_x}, {grid_y})")  # Debug
            if is_valid_move(grid_x, grid_y) and abs(PLAYER_2["positions"][selected_piece][0] - grid_x) + abs(PLAYER_2["positions"][selected_piece][1] - grid_y) == 1:
                PLAYER_2["positions"][selected_piece] = (grid_x, grid_y)
                moved_pieces.append(selected_piece)  # Bu turda hareket eden taşı kaydet
                print(f"Taş hareket ettirildi: {PLAYER_2['positions'][selected_piece]}")  # Debug
                moves_remaining -= 1                
                check_for_eliminations()  # Hamleden sonra hemen taşları kontrol et
                check_wall_captures()

                # Eğer oyuncu hamlelerini tamamladıysa sıra değiştir
                if moves_remaining == 0:
                    print("İnsan oyuncunun sırası tamamlandı!")  # Debug
                    current_player = 1
                selected_piece = None  # Seçimi sıfırla
            else:
                print(f"Geçersiz hamle: ({grid_x}, {grid_y})")  # Debug
                selected_piece = None  # Geçersiz hamlede seçim sıfırlanır

def check_wall_captures():   
    check_wall_captures_left()
    check_wall_captures_right()
    check_wall_captures_top()
    check_wall_captures_bottom()

def check_wall_captures_left():
    """Sol duvar ile rakip taş arasında kalan oyuncu taşlarını sil."""
    for y in range(GRID_SIZE):  # Sol duvar boyunca tüm satırları kontrol et
        # SOL DUVAR - KIRMIZI ÜÇGEN - MAVİ ÇEMBER
        if (0, y) in PLAYER_1["positions"] and (1, y) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((0, y))  # KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Sol Duvar - KIRMIZI ÜÇGEN): (0, {y})")
        
        # SOL DUVAR - MAVİ ÇEMBER - KIRMIZI ÜÇGEN
        elif (0, y) in PLAYER_2["positions"] and (1, y) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((0, y))  # MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Sol Duvar - MAVİ ÇEMBER): (0, {y})")
        
        # SOL DUVAR - KIRMIZI ÜÇGEN - KIRMIZI ÜÇGEN - MAVİ ÇEMBER
        elif (0, y) in PLAYER_1["positions"] and (1, y) in PLAYER_1["positions"] and (2, y) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((0, y))
            PLAYER_1["positions"].remove((1, y))  # İki KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Sol Duvar - İKİ KIRMIZI ÜÇGEN): (0, {y}), (1, {y})")
        
        # SOL DUVAR - MAVİ ÇEMBER - MAVİ ÇEMBER - KIRMIZI ÜÇGEN
        elif (0, y) in PLAYER_2["positions"] and (1, y) in PLAYER_2["positions"] and (2, y) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((0, y))
            PLAYER_2["positions"].remove((1, y))  # İki MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Sol Duvar - İKİ MAVİ ÇEMBER): (0, {y}), (1, {y})")

def check_wall_captures_bottom():
    """Alt duvar ile rakip taş arasında kalan oyuncu taşlarını doğru şekilde sil."""
    for x in range(GRID_SIZE):  # Alt duvar boyunca tüm sütunları kontrol et
        # 1) ALT DUVAR - MAVİ ÇEMBER - KIRMIZI ÜÇGEN
        if (x, GRID_SIZE - 1) in PLAYER_2["positions"] and (x, GRID_SIZE - 2) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((x, GRID_SIZE - 1))  # MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Alt Duvar - MAVİ ÇEMBER): ({x}, {GRID_SIZE - 1})")

        # 2) ALT DUVAR - KIRMIZI ÜÇGEN - MAVİ ÇEMBER
        elif (x, GRID_SIZE - 1) in PLAYER_1["positions"] and (x, GRID_SIZE - 2) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((x, GRID_SIZE - 1))  # KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Alt Duvar - KIRMIZI ÜÇGEN): ({x}, {GRID_SIZE - 1})")

        # 3) ALT DUVAR - MAVİ ÇEMBER - MAVİ ÇEMBER - KIRMIZI ÜÇGEN
        elif (x, GRID_SIZE - 1) in PLAYER_2["positions"] and (x, GRID_SIZE - 2) in PLAYER_2["positions"] and (x, GRID_SIZE - 3) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((x, GRID_SIZE - 1))
            PLAYER_2["positions"].remove((x, GRID_SIZE - 2))  # İki MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Alt Duvar - İKİ MAVİ ÇEMBER): ({x}, {GRID_SIZE - 1}), ({x}, {GRID_SIZE - 2})")

        # 4) ALT DUVAR - KIRMIZI ÜÇGEN - KIRMIZI ÜÇGEN - MAVİ ÇEMBER
        elif (x, GRID_SIZE - 1) in PLAYER_1["positions"] and (x, GRID_SIZE - 2) in PLAYER_1["positions"] and (x, GRID_SIZE - 3) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((x, GRID_SIZE - 1))
            PLAYER_1["positions"].remove((x, GRID_SIZE - 2))  # İki KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Alt Duvar - İKİ KIRMIZI ÜÇGEN): ({x}, {GRID_SIZE - 1}), ({x}, {GRID_SIZE - 2})")

def check_wall_captures_right():
    """Sağ duvar ile rakip taş arasında kalan oyuncu taşlarını doğru şekilde sil."""
    for y in range(GRID_SIZE):  # Sağ duvar boyunca tüm satırları kontrol et
        # 1) KIRMIZI ÜÇGEN - MAVİ ÇEMBER - SAĞ DUVAR
        if (GRID_SIZE - 1, y) in PLAYER_2["positions"] and (GRID_SIZE - 2, y) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((GRID_SIZE - 1, y))  # KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Sağ Duvar - MAVİ ÇEMBER): ({GRID_SIZE - 1}, {y})")
        
        # 2) MAVİ ÇEMBER - KIRMIZI ÜÇGEN - SAĞ DUVAR
        elif (GRID_SIZE - 1, y) in PLAYER_1["positions"] and (GRID_SIZE - 2, y) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((GRID_SIZE - 1, y))  # MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Sağ Duvar - KIRMIZI ÜÇGEN): ({GRID_SIZE - 1}, {y})")
        
        # 3) KIRMIZI ÜÇGEN - MAVİ ÇEMBER - MAVİ ÇEMBER - SAĞ DUVAR
        elif (GRID_SIZE - 1, y) in PLAYER_2["positions"] and (GRID_SIZE - 2, y) in PLAYER_1["positions"] and (GRID_SIZE - 3, y) in PLAYER_1["positions"]:
            PLAYER_1["positions"].remove((GRID_SIZE - 2, y))
            PLAYER_1["positions"].remove((GRID_SIZE - 3, y))  # İki MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Sağ Duvar - İKİ MAVİ ÇEMBER): ({GRID_SIZE - 2}, {y}), ({GRID_SIZE - 3}, {y})")
        
        # 4) MAVİ ÇEMBER - KIRMIZI ÜÇGEN - KIRMIZI ÜÇGEN - SAĞ DUVAR
        elif (GRID_SIZE - 1, y) in PLAYER_1["positions"] and (GRID_SIZE - 2, y) in PLAYER_2["positions"] and (GRID_SIZE - 3, y) in PLAYER_2["positions"]:
            PLAYER_2["positions"].remove((GRID_SIZE - 2, y))
            PLAYER_2["positions"].remove((GRID_SIZE - 3, y))  # İki KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Sağ Duvar - İKİ KIRMIZI ÜÇGEN): ({GRID_SIZE - 2}, {y}), ({GRID_SIZE - 3}, {y})")

def check_wall_captures_top():
    """Üst duvar ile rakip taş arasında kalan oyuncu taşlarını doğru şekilde sil."""
    for x in range(GRID_SIZE):  # Üst duvar boyunca tüm sütunları kontrol et
        # 1) ÜST DUVAR - MAVİ ÇEMBER - KIRMIZI ÜÇGEN
        if (x, 0) in PLAYER_2["positions"] and (x, 1) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((x, 0))  # MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Üst Duvar - MAVİ ÇEMBER): ({x}, 0)")

        # 2) ÜST DUVAR - KIRMIZI ÜÇGEN - MAVİ ÇEMBER
        elif (x, 0) in PLAYER_1["positions"] and (x, 1) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((x, 0))  # KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Üst Duvar - KIRMIZI ÜÇGEN): ({x}, 0)")

        # 3) ÜST DUVAR - MAVİ ÇEMBER - MAVİ ÇEMBER - KIRMIZI ÜÇGEN
        elif (x, 0) in PLAYER_2["positions"] and (x, 1) in PLAYER_2["positions"] and (x, 2) in PLAYER_1["positions"]:
            PLAYER_2["positions"].remove((x, 0))
            PLAYER_2["positions"].remove((x, 1))  # İki MAVİ ÇEMBER silinir
            print(f"Taş yok edildi (Üst Duvar - İKİ MAVİ ÇEMBER): ({x}, 0), ({x}, 1)")

        # 4) ÜST DUVAR - KIRMIZI ÜÇGEN - KIRMIZI ÜÇGEN - MAVİ ÇEMBER
        elif (x, 0) in PLAYER_1["positions"] and (x, 1) in PLAYER_1["positions"] and (x, 2) in PLAYER_2["positions"]:
            PLAYER_1["positions"].remove((x, 0))
            PLAYER_1["positions"].remove((x, 1))  # İki KIRMIZI ÜÇGEN silinir
            print(f"Taş yok edildi (Üst Duvar - İKİ KIRMIZI ÜÇGEN): ({x}, 0), ({x}, 1)")

def check_for_eliminations():
    """Yatay ve dikey taş yok etme kurallarını uygular."""
    global PLAYER_1, PLAYER_2

    # Yatay kontroller
    for y in range(GRID_SIZE):
        x = 0
        while x < GRID_SIZE - 1:
            if (x, y) in PLAYER_1["positions"]:
                end_x = x + 1
                while end_x < GRID_SIZE and (end_x, y) in PLAYER_2["positions"]:
                    end_x += 1
                if end_x < GRID_SIZE and (end_x, y) in PLAYER_1["positions"]:
                    for remove_x in range(x + 1, end_x):
                        PLAYER_2["positions"].remove((remove_x, y))
                        print(f"Taş yok edildi: ({remove_x}, {y})")
                x = end_x
            else:
                x += 1

    for y in range(GRID_SIZE):
        x = 0
        while x < GRID_SIZE - 1:
            if (x, y) in PLAYER_2["positions"]:
                end_x = x + 1
                while end_x < GRID_SIZE and (end_x, y) in PLAYER_1["positions"]:
                    end_x += 1
                if end_x < GRID_SIZE and (end_x, y) in PLAYER_2["positions"]:
                    for remove_x in range(x + 1, end_x):
                        PLAYER_1["positions"].remove((remove_x, y))
                        print(f"Taş yok edildi: ({remove_x}, {y})")
                x = end_x
            else:
                x += 1

    # Dikey kontroller
    for x in range(GRID_SIZE):
        y = 0
        while y < GRID_SIZE - 1:
            if (x, y) in PLAYER_1["positions"]:
                end_y = y + 1
                while end_y < GRID_SIZE and (x, end_y) in PLAYER_2["positions"]:
                    end_y += 1
                if end_y < GRID_SIZE and (x, end_y) in PLAYER_1["positions"]:
                    for remove_y in range(y + 1, end_y):
                        PLAYER_2["positions"].remove((x, remove_y))
                        print(f"Taş yok edildi: ({x}, {remove_y})")
                y = end_y
            else:
                y += 1

    for x in range(GRID_SIZE):
        y = 0
        while y < GRID_SIZE - 1:
            if (x, y) in PLAYER_2["positions"]:
                end_y = y + 1
                while end_y < GRID_SIZE and (x, end_y) in PLAYER_1["positions"]:
                    end_y += 1
                if end_y < GRID_SIZE and (x, end_y) in PLAYER_2["positions"]:
                    for remove_y in range(y + 1, end_y):
                        PLAYER_1["positions"].remove((x, remove_y))
                        print(f"Taş yok edildi: ({x}, {remove_y})")
                y = end_y
            else:
                y += 1

# Ana oyun döngüsü
running = True
clock = pygame.time.Clock()

start_turn()  # İlk tur için moves_remaining ayarla

while running:
    draw_board()
    draw_pieces()
    evaluate_game()
    pygame.display.flip()

    if turn_count >= max_turns:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_player == 2:
            handle_player2_turn(event)

    if current_player == 1:
        handle_player1_turn()
        turn_count += 1
        start_turn()  # Her tur başında moves_remaining hesapla

    clock.tick(10)

pygame.quit()
