# Wordnado Current Development
# Last Edit 11/28/2022 2:47PM

import pygame, sys, random
from pygame.locals import *

pygame.init()

# Game Constants
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

WIDTH = 600
HEIGHT = 900

player = pygame.transform.scale(pygame.image.load('Images/Sprites/worby.png'), (96, 96))

# Background image
bg_img = pygame.image.load('Images/Backgrounds/tornado.jpg')
fps = 60
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

platform = pygame.image.load('Images/Elements/cloud2.png')
platform = pygame.transform.scale(platform, (160, 70))

screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
pygame.display.set_caption('Wordnado')

# Game Variables
player_x = 260
player_y = 750
platforms = [ # [x, y, width, height] of hitboxes
	[250, 850, 160, 12],
	[410, 610, 160, 12],
	[120, 430, 160, 12],
	[375, 290, 160, 12],
	[230, 90, 160, 12]
]
jump = False
y_change = 0
x_change = 0
player_speed = 7

# Update Players Y-Position
def update_player(y_pos):
	global jump
	global y_change
	jump_height = 19
	gravity = .65

	if jump:
		y_change = -jump_height
		jump = False

	y_pos += y_change
	y_change += gravity
	
	return y_pos

# Check for Collisions
def check_collisions(rect_list, j):
	global player_x
	global player_y
	global y_change
	for i in range(len(rect_list)):
		if rect_list[i].colliderect([player_x + 36, player_y + 80, 40, 16]) and jump == False and y_change > 0:
			j = True
	
	return j

# Handle Platform Movement
def update_platforms(platform_list, pos, change):
	if pos < 400 and change < 0:
		for i in range(len(platform_list)):
			platform_list[i][1] -= change
	elif pos < -10:
		for i in range(len(platform_list)):
			platform_list[i][1] += 10
	else:
		pass

	for item in range(len(platform_list)):
		if platform_list[item][1] > 900:
			platform_list[item] = [random.randint(5, 475), random.randint(-60, -40), 160, 12]
	
	return platform_list


# Run Game
running = True
while running == True:
	while True:
		timer.tick(fps)
		screen.blit(bg_img, (0, 0))
		screen.blit(player, (player_x, player_y))
		blocks = []

		# End Screen Set-Up
		endText = pygame.font.Font('freesansbold.ttf', 32).render('Game over', True, black)
		border = pygame.Rect(0, 0, (WIDTH // 3) * 2, (HEIGHT // 3))
		endTextRect = endText.get_rect()
		border.center = (WIDTH / 2, HEIGHT / 2)
		endTextRect.center = border.center

		for i in range(len(platforms)):
			block = pygame.draw.rect(screen, black, platforms[i], 0, 15)
			screen.blit(platform, (block.x, block.y - 35)) # Ties platform hitboxes to platform image
			blocks.append(block)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					x_change = -player_speed
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					x_change = player_speed
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_LEFT:
					x_change = 0
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					x_change = 0

		player_y = update_player(player_y)
		player_x += x_change
		jump = check_collisions(blocks, jump)
		platforms = update_platforms(platforms, player_y, y_change)

		if x_change > 0:
			player = pygame.transform.scale(pygame.image.load('Images/Sprites/worby.png'), (96, 96))
		elif x_change < 0:
			player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('Images/Sprites/worby.png'), (96, 96)), 1, 0)

		if player_y > 900:
			break

		pygame.display.update()
	
	# Replay screen	
	pygame.draw.rect(screen, white, border)
	screen.blit(endText, endTextRect)

	# Add button to retry level
	'''
	if button_is_pressed:
		continue
	else:
		break
	'''

	pygame.display.update()

pygame.quit()