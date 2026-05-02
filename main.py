import pygame
from random import randint

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
jump_sound = pygame.mixer.Sound("gallery/audio/jump.mp3")
back_sound = pygame.mixer.Sound("gallery/audio/backsound.mp3")
back_sound.play(loops=-1)
back_sound.set_volume(0.5)

# Memuat latar belakang dan tanah
skybox = pygame.image.load('gallery/sprites/Sky.png').convert()
ground = pygame.image.load('gallery/sprites/Ground.png').convert()

#Video frames for skeleton
enemy_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy.png").convert_alpha()
enemy_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy2.png").convert_alpha()
enemy_frames = [enemy_frame1, enemy_frame2]
enemy_frame_index = 0
enemy = enemy_frames[enemy_frame_index]

#Video frames for ghost
enemy2_frame1 = pygame.image.load("gallery/sprites/enemies/Enemy2.png").convert_alpha()
enemy2_frame2 = pygame.image.load("gallery/sprites/enemies/Enemy2_2.png").convert_alpha()
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 200)

enemy2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(enemy2_animation_timer, 500)

# Fungsi untuk menampilkan permainan saat aktif
def active_game():
    global player_gravity, obstacle_rect_list, player_rect
    window_screen.blit(skybox, (0,0))         # Tampilkan background
    window_screen.blit(ground, (0, 320))      # Tampilkan tanah/ground
    score = display_score()
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 320:
        player_rect.bottom = 300                   # Tampilkan skor saat ini
    player_animation()                        # Jalankan animasi pemain
    window_screen.blit(player, player_rect)   # Tampilkan pemain di layar
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)

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

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 320:
                window_screen.blit(enemy, obstacle_rect)
            else:
                window_screen.blit(enemy2, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def spawn_enemy():
    global enemy_frame_index, enemy2_frame_index, enemy2_frame2, enemy, enemy2
    if event.type == obstacle_timer:
        if randint(0, 2):
            print('Enemy has been spawned')
            obstacle_rect_list.append(enemy.get_rect(bottomright =(randint(900, 1100), 320)))
        else:
            obstacle_rect_list.append(enemy2.get_rect(bottomright =(randint(900, 1100), 210)))
    if event.type == enemy_animation_timer:
        if enemy_frame_index == 0:
            enemy_frame_index = 1
        else:
            enemy_frame_index = 0
        enemy = enemy_frames[enemy_frame_index]
    
    if event.type == enemy2_animation_timer:
        if enemy2_frame_index == 0:
            enemy2_frame_index = 1
        else:
            enemy2_frame_index = 0
        enemy2 = enemy2_frames[enemy2_frame_index]
# Fungsi animasi pemain agar terlihat berjalan
def player_animation():
    global player_index, player
    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]

# Loop utama game
while True:
    for event in pygame.event.get():
        # Menutup game jika tombol close ditekan atau tombol ESC ditekan
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            spawn_enemy()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    jump_sound.play()
                    player_gravity = -20
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