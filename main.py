import pygame
import engine
import math
import time
import os

os.system("@echo off")
os.system("clear")

pygame.init()
screen = pygame.display.set_mode((160 * 3, 128 * 3), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

def center_x(x: float = 0) -> float:
	return x + screen.get_width() / 2.0

def center_y(y: float = 0) -> float:
	return y + screen.get_height() / 2.0

def center_xy(x: float = 0, y: float = 0) -> float:
	return (center_x(x), center_y(y))

def center_pygame_vector2(vector2: pygame.Vector2 = pygame.Vector2()) -> pygame.Vector2:
	return pygame.Vector2(center_x(vector2.x), center_y(vector2.y))

def vector3_to_pygame(vector3: engine.Vector3 = engine.Vector3()) -> pygame.Vector2:
	z = vector3.z - engine.camera.position.z
	if z < 0:
		vector3 = engine.Vector3(
			-vector3.x,
			-vector3.y,
			-vector3.z
		)
		z = vector3.z - engine.camera.position.z
	return center_pygame_vector2(pygame.Vector2(
		((vector3.x - engine.camera.position.x) / z) if z != 0 else 0,
		(-(vector3.y - engine.camera.position.y) / z) if z != 0 else 0
	) / (engine.camera.fov / 10_000))

def vector2_outside_screen(vector2: pygame.Vector2 = pygame.Vector2()) -> bool:
	x_less = vector2.x < 0
	x_greater = vector2.x > screen.get_width() - 1
	y_less = vector2.y < 0
	y_greater = vector2.y > screen.get_height() - 1
	return x_less or x_greater or y_less or y_greater

def clamp(n, min, max): 
	if n < min: 
		return min
	elif n > max: 
		return max
	else: 
		return n 

def draw(draw_list: list = []):
	sorted_list = []
	for info in draw_list:
		from_position = info[3]
		to_position = info[4]

		center_position = engine.lerp_vector3(from_position, to_position)
		camera_distance = engine.vector3_distance(center_position, camera.position)
		
		info = list(info)
		info.insert(0, camera_distance)
		info = tuple(info)

		sorted_list.append(info)
	
	sorted_list = sorted(sorted_list, key=lambda x: x[0], reverse=True)
	for info in sorted_list:
		distance = info[0]
		draw_type = info[1]
		from_vector2 = info[2]
		to_vector2 = info[3]
		color = info[6]
		outline_size = info[7]

		if draw_type == 0:
			pygame.draw.line(screen, color, from_vector2, to_vector2, round(clamp((1.0 / distance) * (outline_size * 2), 1, 10)))

def draw_line(from_position: engine.Vector3 = engine.Vector3(), to_position: engine.Vector3 = engine.Vector3(), from_offset: engine.Vector3 = engine.Vector3(), to_offset: engine.Vector3 = engine.Vector3(), rotation: engine.Vector3 = engine.Vector3(), rotation_pivot: engine.Vector3 = engine.Vector3(), color: tuple = (255, 255, 255), outline_size: float = 1) -> pygame.Vector2:
	from_pos = engine.rotate_vector3(
	 	from_position,
		rotation,
		rotation_pivot,
		from_offset
	)
	from_pos = engine.rotate_vector3(
	 	from_pos,
		camera.rotation,
		camera.position
	)

	to_pos = engine.rotate_vector3(
	 	to_position,
		rotation,
		rotation_pivot,
		to_offset
	)
	to_pos = engine.rotate_vector3(
	 	to_pos,
		camera.rotation,
		camera.position
	)

	from_clipping = camera.clipping(from_pos)
	center_clipping = camera.clipping(engine.lerp_vector3(from_pos, to_pos))
	to_clipping = camera.clipping(to_pos)

	if from_clipping and center_clipping and to_clipping:
		return to_position, to_offset

	if from_clipping or to_clipping:
		if from_clipping:
			position = from_position
		else:
			position = to_position
		clipping_amount = abs(position.z - camera.position.z)
		
		new_position = engine.Vector3(
			position.x,
			position.y,
			position.z - clipping_amount
		)

		if from_clipping:
			from_position = new_position
		else:
			to_position = new_position

	from_vector2 = vector3_to_pygame(from_pos)
	to_vector2 = vector3_to_pygame(to_pos)

	if vector2_outside_screen(from_vector2) and vector2_outside_screen(pygame.math.Vector2.lerp(from_vector2, to_vector2, 0.5)) and vector2_outside_screen(to_vector2):
		return to_position, to_offset
	
	global draw_list
	draw_list.append((0, from_vector2, to_vector2, from_pos, to_pos, color, outline_size))
	return to_position, to_offset

def draw_box(position: engine.Vector3 = engine.Vector3(), size: engine.Vector3 = engine.Vector3(1, 1, 1), rotation: engine.Vector3 = engine.Vector3(), rotation_pivot: engine.Vector3 = engine.Vector3(), color: tuple = (255, 255, 255), outline_size: float = 1) -> None:
	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		engine.Vector3(size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / -2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		engine.Vector3(size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / 2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / -2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		engine.Vector3(size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		engine.Vector3(size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		engine.Vector3(size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		engine.Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		engine.Vector3(-size.x / 2.0, size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

camera = engine.new_camera()
camera.position.z = -2

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
font = pygame.font.Font('freesansbold.ttf', 16)

rotation = 0
draw_list = []

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEMOTION:
			dx, dy = event.rel
			camera.rotation.y -= dx / 2.0
			camera.rotation.x -= dy / 2.0
			if camera.rotation.x < -90:
				camera.rotation.x = -90
			if camera.rotation.x > 90:
				camera.rotation.x = 90
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_w] or keys[pygame.K_UP]:
		camera.position.x -= math.sin(math.radians(camera.rotation.y)) / 10.0
		camera.position.z += math.cos(math.radians(camera.rotation.y)) / 10.0
	if keys[pygame.K_s] or keys[pygame.K_DOWN]:
		camera.position.x += math.sin(math.radians(camera.rotation.y)) / 10.0
		camera.position.z -= math.cos(math.radians(camera.rotation.y)) / 10.0
	if keys[pygame.K_a] or keys[pygame.K_LEFT]:
		camera.position.x -= math.cos(math.radians(camera.rotation.y)) / 10.0
		camera.position.z -= math.sin(math.radians(camera.rotation.y)) / 10.0
	if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
		camera.position.x += math.cos(math.radians(camera.rotation.y)) / 10.0
		camera.position.z += math.sin(math.radians(camera.rotation.y)) / 10.0
	if keys[pygame.K_SPACE]:
		camera.position.y += 0.1
	if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
		camera.position.y -= 0.1
	if keys[pygame.K_q]:
		camera.rotation.z -= 2
	if keys[pygame.K_e]:
		camera.rotation.z += 2

	screen.fill((0, 0, 0))

	rotation += 1
	rotation = math.fmod(rotation, 360)

	draw_list = []
	draw_box(
		engine.Vector3(-1.5, 2, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(0, rotation, 0)
	)
	draw_box(
		engine.Vector3(1.5, 2, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(rotation, 0, 0)
	)
	draw_box(
		engine.Vector3(0, 2, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(rotation, rotation, 0)
	)
	draw_box(
		engine.Vector3(-1, 3.5, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(45, rotation, 0)
	)
	draw_box(
		engine.Vector3(1, 3.5, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(rotation, 45, 0)
	)
	draw_box(
		engine.Vector3(0, 5, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(0, 0, rotation)
	)
	draw_box(
		engine.Vector3(0, -1, 0),
		engine.Vector3(2, 1, 2),
		outline_size=2
	)
	draw_box(
		engine.Vector3(0, math.sin(time.time_ns() / 1_000_000_000 * 2.0) / 2.0, 0),
		engine.Vector3(1, abs(math.sin(time.time_ns() / 1_000_000_000.0)), 1),
		engine.Vector3(0, rotation, 0),
		engine.Vector3(0, 0, 0),
		(0, 255, 0),
		5
	)
	draw(draw_list)

	fps = round(clock.get_fps())
	fps_color = "red"
	if fps > 10:
		fps_color = "orange"
		if fps > 20:
			fps_color = "yellow"
			if fps > 25:
				fps_color = "green"
	
	text = font.render("FPS: " + str(fps), False, fps_color, "black")
	screen.blit(text, pygame.Vector2(0, 0))
	text = font.render("Render calls: " + str(len(draw_list)), False, "white", "black")
	screen.blit(text, pygame.Vector2(0, 16))

	pygame.display.flip()
	clock.tick(30)

pygame.quit()