import pygame
import pprint
import sys
import math



class new_player:
	def __init__(self, position):
		self.position = position
		self.rotation = 0
		self.max_raycast_range = 10
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
		movement = 0
		if pressed_keys["w"]:
			movement += .05
		if pressed_keys["s"]:
			movement -= .05
		position = list(self.position)
		position[0] += movement * math.sin(self.rotation)
		position[1] += movement * math.cos(self.rotation)
		if not game_map[int(position[0])][int(position[1])]:
			self.position = position
		


	def draw_player(self, screen, tile_size):
		pygame.draw.circle(screen, (255, 0, 0),
			(int(self.position[0] * tile_size), int(self.position[1] * tile_size)),
			5)
		pygame.draw.line(screen, (0, 0, 255), [x * tile_size for x in self.position],
			(int((math.sin(self.rotation) * .2 + self.position[0]) * tile_size),
			int((math.cos(self.rotation) * .2 + self.position[1]) * tile_size)), 4)



	def raycast(self, game_map, screen, tile_size):
		tan = math.tan
		sqrt = math.sqrt
		sin = math.sin
		cos = math.cos
		x = self.position[0]
		y = self.position[1]
		pi = math.pi
		self.distances = []
		for number in range(self.rays):
			angle = self.rotation - self.fov / 2 + self.fov / self.rays * number
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
			min_distance = min(distances)
			pygame.draw.line(screen, (0, 255, 0),
				(x * tile_size, y * tile_size),
				((x + sin(angle) * min_distance) * tile_size, (y + cos(angle) * min_distance) * tile_size),
				)
			self.distances.append(min_distance)



	def draw_raycast(self, screen, screen_size):
		offset = screen_size[0] / 2
		window_height = screen_size[1]
		size_factor = 64
		fog_color = (1, 0, 1)
		for index, distance in enumerate(reversed(self.distances)):
			draw_distance = -distance + 8
			x = index + offset
			color = [distance * .1 * c for c in fog_color]
			pygame.draw.line(screen, color,
				(x, (-(draw_distance * size_factor / 2) + window_height / 2)),
				(x, ((draw_distance * size_factor / 2) + window_height / 2)), 
				)



def raycast_marker(pos):
	global tile_size
	global screen
	pygame.draw.circle(screen, (0, 0, 255), [int(value * tile_size) for value in pos], 5)



game_map = None
def import_map():
	global game_map
	game_map = []
	with open("map", "r") as map_raw:
		for row in map_raw.read().split("\n"):
			final_row = []
			for tile in row.split(" "):
				final_row.append(tile == "#")
			game_map.append(final_row)



def draw_map():
	pass



player_start_position = (1.5, 1.5)
tile_size = 64
screen_size = (1024, 512)
tickrate = 30
keys = {
	119:"w",
	97:"a",
	115:"s",
	100:"d",
	27:"esc"
}



pressed_keys = {key:False for key in keys.values()}
screen = pygame.display.set_mode(screen_size)
import_map()
clock = pygame.time.Clock()
player = new_player(player_start_position)



while True:
	for event in pygame.event.get():
		if event.type == 12:
			pygame.quit()
			sys.exit()
		elif event.type == 2:
			if event.key in keys.keys():
				pressed_keys[keys[event.key]] = True
			else:
				print(event.key)
		elif event.type == 3:
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
	for index_x, row in enumerate(game_map):
		for index_y, tile in enumerate(row):
			if tile:
				pygame.draw.rect(screen, (0, 0, 0), (
					(index_x * tile_size, index_y * tile_size),
					(tile_size, tile_size)
					))
	player.raycast(game_map, screen, tile_size)
	player.draw_player(screen, tile_size)
	player.draw_raycast(screen, screen_size)
	pygame.display.flip()