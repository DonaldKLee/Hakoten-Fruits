import pygame, os, random, time
# Imports the hand tracking code file
import hand_detection

pygame.font.init()


# Sets the width and height of the game window, and the window's name
WIDTH, HEIGHT = 800, 700
WIDTH, HEIGHT = hand_detection.get_camera_size()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Fruit Slicer")

# Load images
apple = pygame.image.load(os.path.join("assets", 'apple.png'))
melon = pygame.image.load(os.path.join("assets", 'melon.png'))
mango = pygame.image.load(os.path.join("assets", 'mango.png'))
coconut = pygame.image.load(os.path.join("assets", 'coconut.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "backgroundtest.png")), (WIDTH,HEIGHT))

# Sword
sword = pygame.image.load(os.path.join("assets", 'sword.png'))
slash_effect = pygame.image.load(os.path.join("assets", "slash_effect.png"))

class fruit:
	COOLDOWN = 30
	ARROW_COOLDOWN = 30
	TRANSFORM_COOLDOWN = 1200

	def __init__(self, x, y, health=200):
		self.x = x
		self.y = y
		self.health = health
		self.fruit_img = None

	def draw(self, window):
		window.blit(self.fruit_img, (self.x, self.y))

	def get_width(self):
		return self.fruit_img.get_width()

	def get_height(self):
		return self.fruit_img.get_height()

class Fruit(fruit):
	COLOR_MAP = {
		"apple": (apple, "apple"),
		"melon": (melon, "melon"),
		"mango": (mango, "mango"),
		"coconut": (coconut, "coconut")
	}
	def __init__(self, x, y, color, health=100):
		super().__init__(x, y, health)
		self.fruit_img, self.fruit_type = self.COLOR_MAP[color]
		# Randomly rotates the fruit
		self.fruit_img = pygame.transform.rotate(self.fruit_img, random.randint(0,180))
		self.mask = pygame.mask.from_surface(self.fruit_img)
	
	def move(self, vel):
		self.y += vel

def main():
	run = True
	FPS = 160
	level = 0
	lives = 10
	
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 40)

	fruits = []
	wave_length = 5
	fruit_vel = 6


	clock = pygame.time.Clock()

	lost = False
	lost_count = 0

	def draw_window():
		# First thing to draw is the background image
		WIN.blit(BG, (0,0)) # 0,0 is top left
		mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
		WIN.blit(sword, (mouse_pos_x - 180, mouse_pos_y - 50))

		# draw text
		lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
		level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		for fruit in fruits:
			fruit.draw(WIN)

		if lost:
			lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
			
			lost_label = lost_font.render("Click here to play again!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2 + 50))


			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					main()

				# If we quit the game, stop running the game
				if event.type == pygame.QUIT: 
					quit()
			

		pygame.display.update()

	while run:
		clock.tick(FPS)
		
		try:
			x,y = hand_detection.open_video()
			pygame.mouse.set_pos(x,y)
		except:

			title_font = pygame.font.SysFont("freesansbold", 60)
			title_label = title_font.render("Warning: Hand not found!", 1, (255,255,255))
			WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))

			pygame.display.update()
			time.sleep(0.5)
			pass

		draw_window()

		if pygame.key.get_pressed()[pygame.K_q]:
			quit()

		if lives <= 0:
			lost = True
			lost_count += 1

		if lost:
			if lost_count > FPS * 3:
				run = False
				exit()
				
			else:
				continue
		
		# Hit boxes
		for fruit in fruits:
			#print(f"{(fruit.x, fruit.y)} and {(pygame.mouse.get_pos())}")
			if fruit.x in range(pygame.mouse.get_pos()[0] - 250, pygame.mouse.get_pos()[0] + 10) and fruit.y in range(pygame.mouse.get_pos()[1] - 100, pygame.mouse.get_pos()[1] - 40):
				
				WIN.blit(slash_effect, (fruit.x, fruit.y)) # Adds the slashing effect
				pygame.display.update()
				fruits.remove(fruit)




		if len(fruits) == 0:
			level += 1
			wave_length += 20
			for i in range(wave_length):
				# 10% chance of spawning the coconut
				if random.randint(0,100) > 90:
					fruit = Fruit(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), color = "coconut")
				else:
					fruit = Fruit(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), color = random.choice(['apple', 'mango', 'melon']))

				fruits.append(fruit)

		for fruit in fruits[:]:
			if fruit.fruit_type == "coconut":
				fruit.move(fruit_vel * 1.5)

			else:
				fruit.move(fruit_vel)

			if fruit.y + fruit.get_height() > HEIGHT:
				lives -= 1
				fruits.remove(fruit)

		for event in pygame.event.get():
			# If we quit the game, stop running the gamhee
			if event.type == pygame.QUIT: 
				quit()


def main_menu():
	title_font = pygame.font.SysFont("comicsans", 35)
	instructions_font = pygame.font.SysFont("comicsans", 25)

	run = True
	while run:
			
		WIN.blit(BG, (0,0))

		title_label = title_font.render("Click anywhere on the game to begin...", 1, (255,255,255))
		WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))

		instruction_label = instructions_font.render("(Make sure your camera can see your hand!)", 1, (255,255,255))
		WIN.blit(instruction_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2 + 50))

		instruction_label = instructions_font.render("Do not play this game if you have Epilepsy", 1, (255,255,255))
		WIN.blit(instruction_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2 + 80))

		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()
			
	pygame.quit()

main_menu()