import sys
import math

import pygame
import load_map



class new_player:
	def __init__(self, position):
		self.position = position
		self.rotation = 0
		self.max_raycast_range = 20
		self.fov = math.radians(70)
		self.rays = 512
		self.min_distance = 0



	def rotate(self, pressed_keys):
		if pressed_keys["a"]:
			self.rotation += .05
		if pressed_keys["d"]:
			self.rotation -= .05
		if self.rotation > math.pi:
			self.rotation -= math.pi * 2
		if self.rotation < -math.pi:
			self.rotation += math.pi * 2



	def move(self, pressed_keys, game_map):
		if pressed_keys["shift"]:
			movement_multiplier = 2
		else:
			movement_multiplier = 1
		movement = 0
		if pressed_keys["w"]:
			movement += .05 * movement_multiplier
		if pressed_keys["s"]:
			movement -= .05 * movement_multiplier
		position = list(self.position)
		position[0] += movement * math.sin(self.rotation)
		position[1] += movement * math.cos(self.rotation)
		if not game_map[int(position[0])][int(position[1])]:
			self.position = position



	def draw_player(self, screen, tile_size):
		pygame.draw.circle(screen, (255, 0, 0),
			(int(self.position[0] * tile_size), int(self.position[1] * tile_size)),
			5)
		pygame.draw.line(screen, (0, 0, 255), [int(x * tile_size) for x in self.position],
			(int((math.sin(self.rotation) * .2 + self.position[0]) * tile_size),
			int((math.cos(self.rotation) * .2 + self.position[1]) * tile_size)), 4)



	def raycast(self, game_map, screen, tile_size, full_window):
		if not full_window:
			rays = self.rays
		else:
			rays = self.rays * 2
		tan = math.tan
		sqrt = math.sqrt
		sin = math.sin
		cos = math.cos
		x = self.position[0]
		y = self.position[1]
		pi = math.pi
		self.distances = []
		for number in range(rays):
			angle = self.rotation - self.fov / 2 + self.fov / rays * number
			if angle != 0:
				if angle > math.pi:
					angle -= math.pi * 2
				if angle < -math.pi:
					angle += math.pi * 2
				distances = [self.max_raycast_range]
				if angle < 0:
					#determine coordinates of next collision with perpendicular lines
					next_full_x = int(x)
					distance_to_next_full_x = x - next_full_x
					y_at_next_full_x = -(distance_to_next_full_x / tan(angle)) + y
					#define new coordinates
					new_x = next_full_x
					new_y = y_at_next_full_x
					#calculate y change for one unit x
					y_change_per_x = -(1 / tan(angle))
					for i in range(self.max_raycast_range):
						try:
							if game_map[new_x - i - 1][int((i * y_change_per_x) + new_y)]:
								distances.append(sqrt((i + x - new_x) ** 2 + (i * y_change_per_x + y_at_next_full_x - y) ** 2))
								break
						except:
							pass
				elif angle > 0:
					#determine coordinates of next collision with perpendicular lines
					next_full_x = int(x) + 1
					distance_to_next_full_x = x - next_full_x
					y_at_next_full_x = -(distance_to_next_full_x / tan(angle)) + y
					#define new coordinates
					new_x = next_full_x
					new_y = y_at_next_full_x
					#calculate y change for one unit x
					y_change_per_x = (1 / tan(angle))
					for i in range(self.max_raycast_range):
						try:
							if game_map[new_x + i][int(new_y + i * y_change_per_x)]:
								distances.append(sqrt((i + new_x - x) ** 2 + (i * y_change_per_x + y_at_next_full_x - y) ** 2))
								break
						except:
							pass
				if angle < -.5 * pi or angle > .5 * pi:
					#determine coordinates of next collision with horizontal lines
					next_full_y = int(y)
					distance_to_next_full_y = y - next_full_y
					x_at_next_full_y = (distance_to_next_full_y / tan(angle - pi * .5)) + x
					#define new coordinates
					new_y = next_full_y
					new_x = x_at_next_full_y
					#calculate x change for one unit y
					x_change_per_y = (1 / tan(angle - pi * .5))
					for i in range(self.max_raycast_range):
						try:
							if game_map[int((i * x_change_per_y) + new_x)][new_y - i - 1]:
								distances.append(sqrt((i * x_change_per_y + x_at_next_full_y - x) ** 2 + (i + y - new_y) ** 2))
								break
						except:
							pass
				elif angle > -.5 * pi and angle < .5 * pi:
					#determine coordinates of next collision with horizontal lines
					next_full_y = int(y) + 1
					distance_to_next_full_y = y - next_full_y
					x_at_next_full_y = (distance_to_next_full_y / tan(angle - pi * .5)) + x
					#define new coordinates
					new_y = next_full_y
					new_x = x_at_next_full_y
					#calculate x change for one unit y
					x_change_per_y = -(1 / tan(angle - pi * .5))
					for i in range(self.max_raycast_range):
						try:
							if game_map[int(new_x + i * x_change_per_y)][new_y + i]:
								distances.append(sqrt((i * x_change_per_y + x_at_next_full_y - x) ** 2 + (i + new_y - y) ** 2))
								break
						except:
							pass
				min_distance = min(distances)
				if not full_window:
					pygame.draw.line(screen, (0, 255, 0),
						(int(x * tile_size), int(y * tile_size)),
						(int((x + sin(angle) * min_distance) * tile_size), int((y + cos(angle) * min_distance) * tile_size)),
						3)
				self.distances.append(min_distance)



	def draw_raycast(self, screen, screen_size, full_window):
		if not full_window:
			offset = screen_size[0] / 2
		else:
			offset = 0
		window_height = screen_size[1]
		size_factor = 512 / self.max_raycast_range
		fog_color = (255, 255, 255)
		for index, distance in enumerate(reversed(self.distances)):
			draw_distance = -distance + self.max_raycast_range
			x = index + offset
			color = [255 - ((1 - distance / self.max_raycast_range) * c) for c in fog_color]
			color = [min(max(c, 0), 255) for c in color]
			pygame.draw.line(screen, color,
				(int(x), int(-(draw_distance * size_factor / 2) + window_height / 2)),
				(int(x), int((draw_distance * size_factor / 2) + window_height / 2)), 
				)



game_map = load_map.load_map()



def draw_map():
	pass



player_start_position = (1.5, 1.5)
tile_size = 32
screen_size = (1024, 512)
tickrate = 30
keys = {
	119:"w",
	97:"a",
	115:"s",
	100:"d",
	27:"esc",
	304:"shift",
	306:"ctrl"
}



pressed_keys = {key:False for key in keys.values()}
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
player = new_player(player_start_position)
full_window = False
window_cooldown = 0



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key in keys.keys():
				pressed_keys[keys[event.key]] = True
			else:
				print(event.key)
		elif event.type == pygame.KEYUP:
			if event.key in keys.keys():
				pressed_keys[keys[event.key]] = False
		else:
			if not event.type in [4]:
				print(event)
	clock.tick(tickrate)
	if pressed_keys["esc"]:
		pygame.quit()
		sys.exit()
	player.rotate(pressed_keys)
	player.move(pressed_keys, game_map)



	screen.fill((255, 255, 255))
	if not full_window:
		for index_x, row in enumerate(game_map):
			for index_y, tile in enumerate(row):
				if tile:
					pygame.draw.rect(screen, (0, 0, 0), (
						(index_x * tile_size, index_y * tile_size),
						(tile_size, tile_size)
						))
		player.draw_player(screen, tile_size)
	player.raycast(game_map, screen, tile_size, full_window)
	player.draw_raycast(screen, screen_size, full_window)
	pygame.display.flip()



	if window_cooldown > 0:
		window_cooldown -= 1
	if pressed_keys["ctrl"] and window_cooldown <= 0:
		full_window = bool(1 - int(full_window))
		window_cooldown = 10
