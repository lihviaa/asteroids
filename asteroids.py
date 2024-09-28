import pygame
import random
import math

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Asteroids")
font = pygame.font.SysFont(None, 36)

# Classe Nave (Player)
class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.angle = 0
        self.speed = 0

    def draw(self):
        points = [
            (self.x + 15 * math.cos(math.radians(self.angle)), self.y - 15 * math.sin(math.radians(self.angle))),
            (self.x + 15 * math.cos(math.radians(self.angle + 120)), self.y - 15 * math.sin(math.radians(self.angle + 120))),
            (self.x + 15 * math.cos(math.radians(self.angle + 240)), self.y - 15 * math.sin(math.radians(self.angle + 240)))
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            self.speed = 5
        elif keys[pygame.K_DOWN]:
            self.speed = -3
        else:
            self.speed = 0

        # Atualiza a posição
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        # Efeito de loop na tela
        if self.x < 0: self.x = 800
        if self.x > 800: self.x = 0
        if self.y < 0: self.y = 600
        if self.y > 600: self.y = 0

# Classe Bala (Bullet)
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def move(self):
        self.x += 10 * math.cos(math.radians(self.angle))
        self.y -= 10 * math.sin(math.radians(self.angle))

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

    def is_off_screen(self):
        return not (0 < self.x < 800 and 0 < self.y < 600)

# Classe Asteroide (Asteroid)
class Asteroid:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.size = random.randint(20, 50)
        self.angle = random.randint(0, 360)
        self.speed = random.random() * 2 + 1

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        # Efeito de loop na tela
        if self.x < 0: self.x = 800
        if self.x > 800: self.x = 0
        if self.y < 0: self.y = 600
        if self.y > 600: self.y = 0

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)

# Classe Gerenciador de Colisão (CollisionManager)
class CollisionManager:
    def check_bullet_asteroid(bullets, asteroids):
        bullets_to_remove = set()
        asteroids_to_remove = set()
        for bullet in bullets:
            for asteroid in asteroids:
                distance = math.hypot(bullet.x - asteroid.x, bullet.y - asteroid.y)
                if distance < asteroid.size:
                    bullets_to_remove.add(bullet)
                    asteroids_to_remove.add(asteroid)
        return bullets_to_remove, asteroids_to_remove

    def check_player_asteroid(player, asteroids):
        for asteroid in asteroids:
            distance = math.hypot(player.x - asteroid.x, player.y - asteroid.y)
            if distance < asteroid.size:
                return True
        return False

# Classe Sistema Principal (Game)
class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.asteroids = []
        self.score = 0

    def create_asteroids(self):
        if len(self.asteroids) < 5:
            self.asteroids.append(Asteroid())

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.angle))

    def run(self):
        running = True
        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.move()
            self.shoot()

            # Movimenta balas e asteroides
            for bullet in self.bullets:
                bullet.move()
            for asteroid in self.asteroids:
                asteroid.move()

            # Colisões
            bullets_to_remove, asteroids_to_remove = CollisionManager.check_bullet_asteroid(self.bullets, self.asteroids)
            
            # Remove balas e asteroides após o cálculo das colisões
            self.bullets = [bullet for bullet in self.bullets if bullet not in bullets_to_remove]
            self.asteroids = [asteroid for asteroid in self.asteroids if asteroid not in asteroids_to_remove]
            
            self.score += len(asteroids_to_remove) * 10

            # Verifica colisão jogador com asteroides
            if CollisionManager.check_player_asteroid(self.player, self.asteroids):
                print("Game Over")
                running = False

            # Desenha objetos na tela
            self.player.draw()
            for bullet in self.bullets:
                bullet.draw()
            for asteroid in self.asteroids:
                asteroid.draw()

            self.create_asteroids()

            # Exibe pontuação
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            pygame.time.delay(30)

        pygame.quit()

# Executa o jogo
game = Game()
game.run()
 