import pygame
import os
import random

pygame.font.init()


# Sets the width and height of the game window, and the window's name
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicer")

# Load images
apple = pygame.image.load(os.path.join("assets", 'apple.png'))
melon = pygame.image.load(os.path.join("assets", 'melon.png'))
mango = pygame.image.load(os.path.join("assets", 'mango.png'))
coconut = pygame.image.load(os.path.join("assets", 'coconut.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH,HEIGHT))


class Ship:
	COOLDOWN = 30
	ARROW_COOLDOWN = 30
	TRANSFORM_COOLDOWN = 1200

	def __init__(self, x, y, health=200):
		self.x = x
		self.y = y
		self.health = health
		self.ship_img = None

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

class Fruit(Ship):
	COLOR_MAP = {
		"red": (apple, "red"),
		"green": (melon, "green"),
		"blue": (mango, "blue"),
		"crown": (coconut, "crown")
	}
	def __init__(self, x, y, color, health=100):
		super().__init__(x, y, health)
		self.ship_img, self.ship_type = self.COLOR_MAP[color]
		
		self.mask = pygame.mask.from_surface(self.ship_img)
	
	def move(self, vel):
		self.y += vel

def main():
	run = True
	FPS = 60
	level = 0
	lives = 10
	
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 60)

	fruits = []
	wave_length = 5
	fruit_vel = 3


	clock = pygame.time.Clock()

	lost = False
	lost_count = 0

	def redraw_window():
		# First thing to draw is the background image
		WIN.blit(BG, (0,0)) # 0,0 is top left
		# draw text
		lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
		level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		for fruit in fruits:
			fruit.draw(WIN)

		if lost:
			lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

		pygame.display.update()

	while run:
		clock.tick(FPS)

		redraw_window()

		if lives <= 0:
			lost = True
			lost_count += 1

		if lost:
			if lost_count > FPS * 3:
				run = False
			else:
				continue
		
		for fruit in fruits:
			#print(f"{(fruit.x, fruit.y)} and {(pygame.mouse.get_pos())}")
			if fruit.x in range(pygame.mouse.get_pos()[0] - 50, pygame.mouse.get_pos()[0] + 50) and fruit.y in range(pygame.mouse.get_pos()[1] - 50, pygame.mouse.get_pos()[1] + 50):
				fruits.remove(fruit)



		if len(fruits) == 0:
			level += 1
			wave_length += 20
			for i in range(wave_length):
				# 10% chance of spawning the crown ship
				if random.randint(0,100) > 90:
					fruit = Fruit(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), color = "crown")
				else:
					fruit = Fruit(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), color = random.choice(['red', 'blue', 'green']))

				fruits.append(fruit)

		for fruit in fruits[:]:
			if fruit.ship_type == "crown":
				fruit.move(fruit_vel * 1.5)

			else:
				fruit.move(fruit_vel)

			if fruit.y + fruit.get_height() > HEIGHT:
				lives -= 1
				fruits.remove(fruit)

		for event in pygame.event.get():
			# If we quit the game, stop running the game
			if event.type == pygame.QUIT: 
				quit()


def main_menu():
	title_font = pygame.font.SysFont("comicsans", 35)

	run = True
	while run:
		WIN.blit(BG, (0,0))
		title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))

	
		WIN.blit(title_label, (WIDTH/2 - 20 - title_label.get_width()/2, 350))

		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()
	pygame.quit()

main_menu()