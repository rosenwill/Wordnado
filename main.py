# Wordnado Current Development

import pygame, sys, random
from pygame.locals import *
import string,time

pygame.init()

# Game Constants

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

WIDTH = 400 #600
HEIGHT = 600 #900

player = pygame.transform.scale(pygame.image.load('Images/Sprites/reggie.png'), (64, 64))

bg_img = pygame.image.load('Images/Backgrounds/tornado.jpg')
fps = 60
timer = pygame.time.Clock()


platform = pygame.image.load('Images/Elements/cloud2.png')
platform = pygame.transform.scale(platform, (140, 60))

screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
pygame.display.set_caption('Wordnado')

# Music Variables

pygame.mixer.init()
pygame.mixer.music.load("Sounds/music.mp3")
pygame.mixer.music.set_volume(0.7)
jump_sound = pygame.mixer.Sound("Sounds/jumpSound.mp3")


# Game Variables

player_x = 175
player_y = 450
platforms = [
	[145, 500, 105, 15],
	[40,  300, 105, 15],
	[285, 100, 105, 15],
]

condition = {
	0: False,
	1: False,
	2: False,
}

jump = False
y_change = 0
x_change = 0
player_speed = 4.5
inputMap = [False, False]

# Update Players Y-Position

def update_player(y_pos):
	global jump
	global y_change
	jump_height = 16.5
	gravity = .65

	if jump:
		y_change = -jump_height
		jump = False

	y_pos += y_change
	if y_change < 14:
		y_change += gravity

	if y_pos < -25:
		y_pos = y_pos - (y_pos + 25)

	return y_pos

# Check for Collisions

def check_collisions(rect_list, j):
	global player_x
	global player_y
	global y_change
	for i in range(len(rect_list)):
		if rect_list[i].colliderect([player_x + 24, player_y + 60, 20, 8]) and jump == False and y_change > 0:
			pygame.mixer.Sound.play(jump_sound)
			j = True
	return j

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
scoreX = 8
scoreY = 8

# Random letters
def create_letter():
	letter = random.sample(string.ascii_uppercase)

# Time Limit / Clock
clock = pygame.time.Clock()
start_time = time.time()
counter = 45
timeX = WIDTH - 50
timeY = 10
pygame.time.set_timer(pygame.USEREVENT, 45)
font = pygame.font.Font('freesansbold.ttf', 28)

# Handle Platform Movement

def update_platforms(platform_list, pos, change):
	if pos < 300 and change < 0:
		for i in range(len(platform_list)):
			platform_list[i][1] += -change
	elif (pos < 100 and change < 0) or (pos < 5):
		for i in range(len(platform_list)):
			platform_list[i][1] += 10
	else:
		pass
	for item in range(len(platform_list)):
		if platform_list[item][1] > 600:
			condition[item] = False
			platform_list[item] = [random.randint(5, 300), 0, 105, 15]
			if random.randint(0, 100) < 25:
				condition[item] = True
	return platform_list


# Run Game

running = True
while running == True:
	pygame.mixer.music.play()
	exit = False
	while True:
		timer.tick(fps)
		screen.blit(bg_img, (0, 0))
		screen.blit(player, (player_x, player_y))
		blocks = []

		# Level Over Screen Set-Up
		endText = pygame.font.Font('freesansbold.ttf', 40).render('Level Over', True, (174, 201, 220))
		retry1Text = pygame.font.Font('freesansbold.ttf', 14).render('Press the R key to restart', True, (174, 201, 220))
		retry2Text = pygame.font.Font('freesansbold.ttf', 14).render('or press Enter to exit the level', True, (174, 201, 220))
		border = pygame.Rect(0, 0, (WIDTH // 3) * 2, (HEIGHT // 3))
		border.center = (WIDTH / 2, HEIGHT / 2)
		endTextRect = endText.get_rect()
		endTextRect.center = border.center
		endTextRect.y = endTextRect.y - 30
		retry1TextRect, retry2TextRect = retry1Text.get_rect(), retry2Text.get_rect()
		retry1TextRect.center = retry2TextRect.center = border.center
		retry1TextRect.y, retry2TextRect.y = retry1TextRect.y + 20, retry2TextRect.y + 45

		for i in range(len(platforms)):
			block = pygame.draw.rect(screen, black, platforms[i], 0, 15)
			screen.blit(platform, (block.x - 17, block.y - 25))
			blocks.append(block)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:    
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					inputMap[0] = True;
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					inputMap[1] = True;
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					inputMap[0] = False;
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					inputMap[1] = False;
			if event.type == pygame.USEREVENT: # timer
				counter -= fps / 2000

		if inputMap[0]: x_change = -player_speed
		if inputMap[1]: x_change = player_speed
		if not inputMap[0] and not inputMap[1]: x_change = 0

		# Display score
		screen.blit(font.render("Score: " + str(score_value), True, white), (scoreX, scoreY))

		# Display timer
		screen.blit(font.render("0" if counter <= 0 else str(round(counter)), True, white), (timeX if counter >= 9.5 else timeX + 20, timeY))
		pygame.display.flip()
		if counter < 0:
			break

		player_y = update_player(player_y)
		player_x += x_change
		jump = check_collisions(blocks, jump)
		platforms = update_platforms(platforms, player_y, y_change)

		if x_change > 0:
			player = pygame.transform.scale(pygame.image.load('Images/Sprites/reggie.png'), (64, 64))
		elif x_change < 0:
			player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Images/Sprites/reggie.png'), (64, 64)), 1, 0)

		if player_y > HEIGHT:
			break

		for item in range(len(platforms)):
			if condition[item] == True:
				pass

		pygame.display.update()

	while not exit:
		# Replay screen
		inputMap = [False, False]
		pygame.draw.rect(screen, (90, 108, 122), border)
		pygame.draw.rect(screen, (43, 50, 54), border, 5)
		screen.blit(endText, endTextRect)
		screen.blit(retry1Text, retry1TextRect)
		screen.blit(retry2Text, retry2TextRect)

		# Retry options -> R key and Enter key
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_r: # R Key = Restart level
					exit = True
					# Reset changed values to default values
					player_x = 175
					player_y = 420
					timeX = WIDTH - 50
					counter = 45
					platforms = [
						[145, 500, 105, 15],
						[40,  300, 105, 15],
						[285, 100, 105, 15],]
				elif event.key == pygame.K_RETURN: # Enter Key = Exit level
					exit = True
					running = False

		pygame.display.update()

pygame.quit()