import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 50
TILE_SIZE = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перемещение героя")


def load_image(filename, colorkey=None):
    try:
        image = pygame.image.load(filename)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {filename}: {e}")
        sys.exit()
    if colorkey is not None:
        image = image.convert()
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


BACKGROUND = load_image("fon.jpg")
WALL = load_image("box.png")
GRASS = load_image("grass.png")
HERO_IMG = load_image("mar.png")


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen, clock):
    intro_text = [
        "Перемещение героя",
        "Герой двигается",
        "Карта на месте"
    ]
    font = pygame.font.Font(None, 50)
    text_coord = 200
    bg_scaled = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
    screen.blit(bg_scaled, (0, 0))
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color("white"))
        rect = string_rendered.get_rect(center=(WIDTH // 2, text_coord))
        screen.blit(string_rendered, rect)
        text_coord += 60
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        clock.tick(FPS)


def load_level(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            level_map = [line.rstrip("\n") for line in file]
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        terminate()
    max_width = max(len(row) for row in level_map)
    return [row.ljust(max_width, ".") for row in level_map]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y, group, off_x, off_y):
        super().__init__(group)
        if tile_type == "#":
            self.image = WALL
        else:
            self.image = GRASS
        self.rect = self.image.get_rect()
        self.rect.x = off_x + x * TILE_SIZE
        self.rect.y = off_y + y * TILE_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, group, off_x, off_y):
        super().__init__(group)
        self.image = HERO_IMG
        self.rect = self.image.get_rect()
        self.hero_width = self.rect.width
        self.hero_height = self.rect.height
        self.x = x
        self.y = y
        self.off_x = off_x
        self.off_y = off_y
        offset_x = (TILE_SIZE - self.hero_width) // 2
        offset_y = (TILE_SIZE - self.hero_height) // 2
        self.rect.x = off_x + x * TILE_SIZE + offset_x
        self.rect.y = off_y + y * TILE_SIZE + offset_y

    def move(self, dx, dy, level_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(level_map) and 0 <= new_x < len(level_map[0]):
            if level_map[new_y][new_x] != "#":
                self.x = new_x
                self.y = new_y
                offset_x = (TILE_SIZE - self.hero_width) // 2
                offset_y = (TILE_SIZE - self.hero_height) // 2
                self.rect.x = self.off_x + self.x * TILE_SIZE + offset_x
                self.rect.y = self.off_y + self.y * TILE_SIZE + offset_y


def generate_level(level_map):
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level_width = len(level_map[0]) * TILE_SIZE
    level_height = len(level_map) * TILE_SIZE
    off_x = (WIDTH - level_width) // 2
    off_y = (HEIGHT - level_height) // 2
    player = None
    for y, row in enumerate(level_map):
        for x, cell in enumerate(row):
            Tile(cell if cell == "#" else ".", x, y, tiles_group, off_x, off_y)
            if cell == "@":
                player = Player(x, y, player_group, off_x, off_y)
    all_sprites.add(tiles_group, player_group)
    return player, tiles_group, player_group, all_sprites


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, rect):
        return rect.move(self.dx, self.dy)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def main():
    clock = pygame.time.Clock()
    start_screen(screen, clock)
    filename = input("Введите имя файла с уровнем: ")
    level_map = load_level(filename)
    screen.fill((0, 0, 0))
    pygame.display.flip()
    player, tiles_group, player_group, all_sprites = generate_level(level_map)
    camera = Camera()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, level_map)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, level_map)
                elif event.key == pygame.K_UP:
                    player.move(0, -1, level_map)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, level_map)
        camera.update(player)
        screen.fill((0, 0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite.rect))
        pygame.display.flip()
        clock.tick(FPS)
    terminate()


if __name__ == "__main__":
    main()
