import pygame

# Inisialisasi semua modul pygame
pygame.init()

# Ukuran layar permainan
frame_size_x = 800 
frame_size_y = 400 

# Membuat jendela/tampilan utama game
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

# Menambahkan judul pada jendela game
pygame.display.set_caption("Running Game")

# Membuat objek clock untuk mengatur FPS (frame per second)
clock = pygame.time.Clock()
FPS = 60  # Jumlah frame per detik

# Mengatur font yang akan digunakan
font = pygame.font.Font("gallery/fonts/Pixeltype.ttf", 32)

# Variabel untuk menyimpan waktu mulai permainan
start_time = 0

# Status permainan: aktif atau tidak
game_active = False  # Permainan belum aktif saat pertama kali dijalankan

# Memuat sprite (gambar) untuk animasi berjalan pemain
player_walk_1 = pygame.image.load("gallery/sprites/player/Player.png").convert_alpha()
player_walk_2 = pygame.image.load("gallery/sprites/player/Player2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]  # Disimpan dalam list untuk animasi
player_index = 0  # Indeks awal animasi pemain
player = player_walk[player_index]  # Gambar pemain saat ini

# Gambar pemain saat melompat
player_jump = pygame.image.load("gallery/sprites/player/Player3.png").convert_alpha()

# Mengatur posisi awal pemain di layar
player_rect = player.get_rect(midbottom=(80, 300))

# Variabel gravitasi untuk pemain (digunakan saat lompat)
player_gravity = 0

# Memuat latar belakang dan tanah
skybox = pygame.image.load('gallery/sprites/Sky.png').convert()
ground = pygame.image.load('gallery/sprites/Ground.png').convert()

# Fungsi untuk menampilkan permainan saat aktif
def active_game():
    global player_gravity 
    window_screen.blit(skybox, (0,0))         # Tampilkan background
    window_screen.blit(ground, (0, 320))      # Tampilkan tanah/ground
    score = display_score()                   # Tampilkan skor saat ini
    player_animation()                        # Jalankan animasi pemain
    window_screen.blit(player, player_rect)   # Tampilkan pemain di layar

# Fungsi untuk menampilkan layar saat permainan belum dimulai / tidak aktif
def inactive_game():
    window_screen.fill((64, 64, 64))  # Latar belakang warna abu-abu
    window_screen.blit(player, (frame_size_x // 2 - 30 , frame_size_y//2 - 30 ))  # Tampilkan pemain di tengah layar

    # Tampilkan judul game
    game_name = font.render("Running Game", False,"white")
    game_name = pygame.transform.scale2x(game_name)  # Perbesar ukuran tulisan
    game_name_rect = game_name.get_rect(center=(400,80))

    # Tampilkan pesan untuk memulai permainan
    game_message = font.render("Press Space to start", False, "white")
    game_message_rect = game_message.get_rect(center = (400, 300))

    # Tampilkan semua elemen teks ke layar
    window_screen.blit(game_name, game_name_rect)
    window_screen.blit(game_message, game_message_rect)

# Fungsi untuk menghitung dan menampilkan skor berdasarkan waktu bermain
def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time  # Konversi waktu ke skor
    score = font.render(f"{current_time}", False, "white")  # Render teks skor
    score_rect = score.get_rect(center = (400, 50))  # Atur posisi skor di layar
    window_screen.blit(score, score_rect)  # Tampilkan skor
    return current_time  # Kembalikan nilai skor

# Fungsi animasi pemain agar terlihat berjalan
def player_animation():
    global player_index, player
    player_index += 0.1  # Tambah indeks sedikit demi sedikit untuk animasi halus
    if player_index >= len(player_walk):  # Jika melebihi jumlah frame animasi, reset ke 0
        player_index = 0
    player = player_walk[int(player_index)]  # Update gambar pemain

# Loop utama game
while True:
    for event in pygame.event.get():
        # Menutup game jika tombol close ditekan atau tombol ESC ditekan
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            # Jika game sedang aktif, tidak ada aksi khusus di sini
            print("Game Active")
        else:
            # Jika game belum aktif, mulai game saat tombol spasi ditekan
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/600)  # Simpan waktu mulai game

    # Tampilkan layar permainan sesuai status game
    if game_active:
        active_game()  # Jalankan tampilan saat game aktif
    else:
        inactive_game()  # Jalankan tampilan saat game belum dimulai
        player_animation()  # Tetap jalankan animasi pemain di layar awal

    pygame.display.update()  # Perbarui tampilan
    clock.tick(FPS)  # Batasi kecepatan frame per detik sesuai nilai FPS