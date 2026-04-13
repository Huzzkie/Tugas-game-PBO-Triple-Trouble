import pygame
import sys

pygame.init()
WIDTH = 1000
HEIGHT = 800

clock = pygame.time.Clock() #Mengambil waktu
fps = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triple Trouble")

 
#Load Sprite/Images
sun_img = pygame.image.load('Sprite/sun.png') #Load gambar statis
bg_img = pygame.image.load('Sprite/sky.png')


#Declare warna
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)


tileSize = 50 #Untuk menghitung tile pada indeks World_Data, memudahkan level editing

def draw_grid(): #Menggambar grid, di layar, bisa digunakan untuk menghitung X dan Y. Utamanya untuk world editor
    for line in range (0, 20):
        pygame.draw.line(screen, WHITE, (0, line * tileSize), (WIDTH, line * tileSize))
        pygame.draw.line(screen, WHITE, (line * tileSize, 0), (line * tileSize, HEIGHT))

class World():
    def __init__(self,data):
        self.tile_list = []
        self.portal_rect = None #Untuk menyimpan posisi portal (pintu)

        #Load Data sprite untuk World
        rumput = pygame.image.load('Sprite/grass.png')
        tanah = pygame.image.load('Sprite/dirt.png')
        portal = pygame.image.load('Sprite/portal.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(rumput, (tileSize, tileSize)) #Ubah ukuran sprite sesuai ukuran tile
                    img_rect = img.get_rect() #Untuk collision
                    img_rect.x = col_count * tileSize #Menentukan Posisi X dan Y dari blok yang dipasang
                    img_rect.y = row_count * tileSize
                    tile = (img, img_rect) #Tile adalah sebuah Tuple, 0 untuk gambarnya, dan 1 untuk menyimpan kotak kordinat dari kotak tersebut
                    self.tile_list.append(tile) #Taruh file di indeks paling belakang 
                if tile == 2:
                    img = pygame.transform.scale(tanah, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tileSize
                    img_rect.y = row_count * tileSize
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(portal, (tileSize, tileSize))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tileSize
                    img_rect.y = row_count * tileSize
                    self.tile_list.append((img, img_rect))
                    self.portal_rect = img_rect
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile [1])

    def check_collision(self, rect):
        for tile in self.tile_list:
            if self.portal_rect and tile[1] == self.portal_rect:
                continue
            if tile[1].colliderect(rect):
                return True
        return False

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)

class Player:
    def __init__(self, x, y, char_type, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Animasi Variabel
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 1 # 1: Kanan, -1: Kiri
        
        # Load Animasi (Asumsi ada 4 frame: 1, 2, 3, 4)
        for num in range(1, 5):
            img_right = pygame.image.load(f'Sprite/{char_type}{num}.png') #gunakan f-string untuk menentukan tipe char dan nomor animasinya
            img_right = pygame.transform.scale(img_right, (self.width, self.height))
            img_left = pygame.transform.flip(img_right, True, False) #Tinggal flip img right
            self.images_right.append(img_right)
            self.images_left.append(img_left) #Append untuk menaruh animasi di indeks paling belakang
        
        self.image = self.images_right[self.index]
        
        # Movement & Gravity
        self.vel_y = 0
        self.jump_power = -15 #Jump power pakai negatif karena di Pygame Y positif kebawah
        self.speed = 5
        self.in_air = True

    def move(self, keys, world):
        dx = 0
        dy = 0
        walk_cooldown = 15 #Untuk membatasi kecepatan perpindahan animasi player
        moving = False

        # Input Horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.counter += 1
            self.direction = -1
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.counter += 1
            self.direction = 1
            moving = True

        # Input Jump
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and not self.in_air:
            self.vel_y = self.jump_power
            self.in_air = True

        # Logika Animasi
        if not moving:
            self.counter = 0
            self.index = 0
        
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
        
        # Update Image berdasarkan arah
        if self.direction == 1:
            self.image = self.images_right[self.index]
        else:
            self.image = self.images_left[self.index]

        # Tambah Gravitasi
        self.vel_y += 1 #Semakin lama jatuh semakin cepat
        if self.vel_y > 10: self.vel_y = 10 #agar kecepatan jatuh tidak terlalu cepat
        dy += self.vel_y

        # Cek Tabrakan X
        self.x += dx
        if world.check_collision(self.get_rect()):
            self.x -= dx

        # Cek Tabrakan Y
        self.y += dy
        self.in_air = True
        for tile in world.tile_list:
            if world.portal_rect and tile[1] == world.portal_rect: #Agar player tidak collide dengan portal
                continue
                
            if tile[1].colliderect(self.get_rect()):
                if self.vel_y > 0: # Jatuh
                    self.y = tile[1].top - self.height
                    self.vel_y = 0
                    self.in_air = False
                elif self.vel_y < 0: # Loncat mentok plafon
                    self.y = tile[1].bottom
                    self.vel_y = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height) #Hitbox dari player

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

#Subclass / Kelas anak dari Player
class Cat(Player):
    def __init__(self, x, y):
        super().__init__(x, y, "cat", 40, 40) #super x, y, char type, char width, char height
        self.speed = 8
        self.jump_power = -18

class Human(Player):
    def __init__(self, x, y):
        super().__init__(x, y, "human", 50, 70)
        self.speed = 5
        self.jump_power = -15

class Bear(Player):
    def __init__(self, x, y):
        super().__init__(x, y, "bear", 90, 90)
        self.speed = 3
        self.jump_power = -12


p_cat = Cat(100, 100) #Titik spawn awal dari player
p_human = Human(100, 100)
p_bear = Bear(100, 100)
player = p_human #Form pertama dari player

# Variabel Status Game
game_over = 0 # 0: Main, 1: Menang

# Font untuk UI
font = pygame.font.SysFont('Futura', 50)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

#Game loop utama
running = True
while running:

    clock.tick(fps) #Pembatas FPS, agar program tidak menjalankan kode secepat mungkin

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg_img, (0, 0)) #Masukkan dulu background statis
    screen.blit(sun_img, (200, 100))
    
    world.draw() #panggil fungsi untuk gambar world
    if game_over == 0:
        keys = pygame.key.get_pressed()
        player.move(keys, world)
        player.draw(screen)

        # CEK COLLISION PINTU (Khusus Human)
        if isinstance(player, Human): #Agar hanya manusia yang bisa masuk ke portal
            if world.portal_rect and player.get_rect().colliderect(world.portal_rect):
                game_over = 1
    elif game_over == 1:
        draw_text("LEVEL CLEARED!", font, BLUE, 350, 300)
        
        # Tombol Retry
        retry_rect = pygame.Rect(420, 400, 150, 50)
        pygame.draw.rect(screen, GREEN, retry_rect)
        draw_text("RETRY", font, WHITE, 435, 405)

        # Tombol Next Level
        next_rect = pygame.Rect(420, 470, 250, 50)
        pygame.draw.rect(screen, BROWN, next_rect)
        draw_text("NEXT LEVEL", font, WHITE, 435, 475)

        # Logika Klik Tombol
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]: # Klik kiri
            if retry_rect.collidepoint(pos):
                player.x, player.y = 100, 100 # Reset posisi
                game_over = 0
            if next_rect.collidepoint(pos):
                print("Coming Soon!") # Bisa diganti jadi draw_text di layar
                draw_text("COMING SOON!", font, RED, 380, 550)

    #Line agar karakter bisa berubah jadi berbagai Form
    if keys[pygame.K_1]: 
        p_cat.x, p_cat.y = player.x, player.y  # Transfer posisi dari karakter lama ke karakter baru
        player = p_cat
    elif keys[pygame.K_2]:
        p_human.x, p_human.y = player.x, player.y
        player = p_human
    elif keys[pygame.K_3]:
        p_bear.x, p_bear.y = player.x, player.y
        player = p_bear

    
    #draw_grid() #Gambar grid untuk membantu world editing

    pygame.display.update()

pygame.quit()
sys.exit()