import pygame, os, random, time
import hand_detection # Imports the hand tracking code file

pygame.font.init()


# Sets the width and height of the game window to the size of the camera
WIDTH, HEIGHT = hand_detection.get_camera_size()
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 

pygame.display.set_caption("Hakoten Fruits") # Name of the window

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
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.fruit_img = None
	
	# Draws the fruit onto the game
	def draw(self, window):
		window.blit(self.fruit_img, (self.x, self.y))

	# Gets the width and height of the fruits
	def get_width(self):
		return self.fruit_img.get_width()
	def get_height(self):
		return self.fruit_img.get_height()

class Fruit(fruit):
	# A dictionary containing the fruit's parameters (image, type of fruit)
	COLOR_MAP = {
		"apple": (apple, "apple"),
		"melon": (melon, "melon"),
		"mango": (mango, "mango"),
		"coconut": (coconut, "coconut")
	}
	def __init__(self, x, y, color):
		super().__init__(x, y)

		self.fruit_img, self.fruit_type = self.COLOR_MAP[color] # Gets the fruit's image and type from the dictionary
		
		# Rotates the fruit by a random degree
		self.fruit_img = pygame.transform.rotate(self.fruit_img, random.randint(0,180))
		self.mask = pygame.mask.from_surface(self.fruit_img)
	
	# Moves the fruits down
	def move(self, vel):
		self.y += vel

# The main function that initalizes the game
def main():
	run = True
	# Initalizes the game's parameters
	FPS = 160
	level = 0
	lives = 10 # Number of fruits that the user can miss before losing
	
	# Fonts for text
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 40)

	fruits = []
	wave_length = 5 # Number of fruits that will spawn per wave
	fruit_vel = 6 # Veolocity of fruits


	clock = pygame.time.Clock()

	lost = False
	lost_count = 0 # Number of fruits the user missed

	# Redraws the game's graphics
	def draw_window():
		# First thing to draw is the background image
		WIN.blit(BG, (0,0)) # 0,0 is top left

		mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos() # Gets the x and y cordinates of the mouse
		WIN.blit(sword, (mouse_pos_x - 180, mouse_pos_y - 50)) # Places the sword where ever the mouse is

		# Draws text
		lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
		level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		# For every fruit spawned, draw it
		for fruit in fruits:
			fruit.draw(WIN)

		# If the user loses, show the following text
		if lost:
			lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))
			
			lost_label = lost_font.render("Click here to play again!", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2 + 50))

			# If the user clicks on the screen, reruns the game
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					main()

				# If the user quits the game, stop running the game
				if event.type == pygame.QUIT: 
					quit()
			
		pygame.display.update()

	# While the game is running
	while run:
		clock.tick(FPS)
		
		# Tries to detect the position of the hand
		try:
			x,y = hand_detection.open_video() # Runs the hand detection machine learning model
			pygame.mouse.set_pos(x,y) # Moves the mouse to where ever the user's hand is

		# If the psition of the hand is not found, ignore it, and continue running the game
		except:
			# Show a pop up telling the user that their hand is not found
			title_font = pygame.font.SysFont("freesansbold", 60)
			title_label = title_font.render("Warning: Hand not found!", 1, (255,255,255))
			WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))

			pygame.display.update()
			time.sleep(0.5) # Pauses the game for half a second so the user has time to bring their hand back into the camera
			pass

		draw_window()

		# If the user runs out of lives, they lose
		if lives <= 0:
			lost = True
			lost_count += 1

		# If the user loses, stop the game
		if lost:
			if lost_count > FPS * 3:
				run = False
			else:
				continue
		
		# Hit boxes
		for fruit in fruits:
			# If the sword is touching the fruit, removes the fruit from the game
			if fruit.x in range(pygame.mouse.get_pos()[0] - 250, pygame.mouse.get_pos()[0] + 10) and fruit.y in range(pygame.mouse.get_pos()[1] - 100, pygame.mouse.get_pos()[1] - 40):
				
				WIN.blit(slash_effect, (fruit.x, fruit.y)) # Adds the slashing effect
				pygame.display.update() # Updates the game so that the slashing effect appears
				fruits.remove(fruit) # Removes the fruit

		# If all the fruits are gone, increase the level, and wave length
		if len(fruits) == 0:
			level += 1
			wave_length += 20
			for i in range(wave_length):
				# 10% chance of spawning the coconut
				if random.randint(0,100) > 90:
					fruit = Fruit(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), color = "coconut")
				else: # 90% chance of spawning other fruits
					fruit = Fruit(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), color = random.choice(['apple', 'mango', 'melon']))

				fruits.append(fruit)
		
		for fruit in fruits[:]:
			# If the fruit is a coconut, increase it's velocity by 1.5
			if fruit.fruit_type == "coconut":
				fruit.move(fruit_vel * 1.5)
			else:
				fruit.move(fruit_vel)

			# If the fruit reaches the bottom of the game, the user loses 1 life and the fruit is removed
			if fruit.y + fruit.get_height() > HEIGHT:
				lives -= 1
				fruits.remove(fruit)
	
		for event in pygame.event.get():
			# If we quit the game, stop running the game
			if event.type == pygame.QUIT: 
				quit()

# The start menu that users see when they run the game
def start_menu():
	title_font = pygame.font.SysFont("comicsans", 35)
	instructions_font = pygame.font.SysFont("comicsans", 25)

	run = True
	while run:
		# Displays the background of the game, and it's instructions
		WIN.blit(BG, (0,0))

		title_label = title_font.render("Click anywhere on the game to begin...", 1, (255,255,255))
		WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))

		instruction_label = instructions_font.render("(Make sure your camera can see your hand!)", 1, (255,255,255))
		WIN.blit(instruction_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2 + 50))

		instruction_label = instructions_font.render("Do not play this game if you have Epilepsy", 1, (255,255,255))
		WIN.blit(instruction_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2 + 80))

		pygame.display.update()
		for event in pygame.event.get():
			# Ends the game if the user closes out of it
			if event.type == pygame.QUIT:
				run = False
			# Starts the game if the user clicks on the screen
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()
	# Stops the game
	pygame.quit()

# Runs the start menu for the game
start_menu()