import pygame
import engine
import math
import time
import os

os.system("@echo off")
os.system("clear")

pygame.init()
screen = pygame.display.set_mode((160 * 3, 128 * 3))
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
	return center_pygame_vector2(pygame.Vector2(
		((vector3.x - engine.camera.position.x) / z) if z != 0 else 0,
		(-(vector3.y - engine.camera.position.y) / z) if z != 0 else 0
	) * engine.camera.fov)

def vector2_outside_screen(vector2: pygame.Vector2 = pygame.Vector2()) -> bool:
	x_less = vector2.x < 0
	x_greater = vector2.x > screen.get_width() - 1
	y_less = vector2.y < 0
	y_greater = vector2.y > screen.get_height() - 1
	return x_less or x_greater or y_less or y_greater

def draw_line(from_position: engine.Vector3 = engine.Vector3(), to_position: engine.Vector3 = engine.Vector3(), from_offset: engine.Vector3 = engine.Vector3(), to_offset: engine.Vector3 = engine.Vector3(), rotation: engine.Vector3 = engine.Vector3(), rotation_pivot: engine.Vector3 = engine.Vector3()) -> pygame.Vector2:
	rot = engine.add_vector3(rotation, camera.rotation)
	rot_pivot = engine.add_vector3(camera.position, rotation_pivot)
	
	# from_position = engine.subtract_vector3(from_position, camera.position)
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
	# from_position = engine.add_vector3(from_position, camera.position)

	# to_position = engine.subtract_vector3(to_position, camera.position)
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
	# to_position = engine.add_vector3(to_position, camera.position)

	if camera.clipping(from_pos) or camera.clipping(to_pos):
		return to_position, to_offset

	from_vector2 = vector3_to_pygame(from_pos)
	to_vector2 = vector3_to_pygame(to_pos)

	if vector2_outside_screen(from_vector2) and vector2_outside_screen(pygame.math.Vector2.lerp(from_vector2, to_vector2, 0.5)) and vector2_outside_screen(to_vector2):
		return to_position, to_offset
	
	global render_calls
	render_calls += 1
	pygame.draw.line(screen, (255, 255, 255), from_vector2, to_vector2)
	return to_position, to_offset

def draw_triangle(point_a: engine.Vector3 = engine.Vector3(), point_b: engine.Vector3 = engine.Vector3(), point_c: engine.Vector3 = engine.Vector3()) -> None:
	draw_line(point_a, point_b)
	draw_line(point_b, point_c)
	draw_line(point_c, point_a)

def draw_rectangle(point_a: engine.Vector3 = engine.Vector3(), point_b: engine.Vector3 = engine.Vector3(), point_c: engine.Vector3 = engine.Vector3(), point_d: engine.Vector3 = engine.Vector3()) -> None:
	draw_line(point_a, point_b)
	draw_line(point_b, point_c)
	draw_line(point_c, point_d)
	draw_line(point_d, point_a)

def draw_box(position: engine.Vector3 = engine.Vector3(), size: engine.Vector3 = engine.Vector3(1, 1, 1), rotation: engine.Vector3 = engine.Vector3(), rotation_pivot: engine.Vector3 = engine.Vector3()) -> None:
	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		engine.Vector3(size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / -2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		engine.Vector3(size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / 2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		last_position,
		engine.Vector3(-size.x / 2.0, size.y / -2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		engine.Vector3(-size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		engine.Vector3(size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		engine.Vector3(size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		engine.Vector3(size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		engine.Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot
	)

	last_position, last_offset = draw_line(
		engine.Vector3(-size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		engine.Vector3(-size.x / 2.0, size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot
	)

camera = engine.new_camera()
camera.position.z = -2
hai = 0

render_calls = 0

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
font = pygame.font.Font('freesansbold.ttf', 16)

y_velocity = 0

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
			if event.key == pygame.K_SPACE:
				y_velocity = 0.15
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
	# if keys[pygame.K_SPACE]:
	# 	camera.position.y += 0.1
	if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
		camera.position.y -= 0.1
	if camera.position.x > 2:
		camera.position.x = 2
	if camera.position.x < -2:
		camera.position.x = -2
	if camera.position.y > 2:
		camera.position.y = 2
		y_velocity = 0
	camera.position.y += y_velocity
	if camera.position.y < -2:
		camera.position.y = -2
		y_velocity = 0
	else:
		y_velocity -= 0.01
	if camera.position.z > 2:
		camera.position.z = 2
	if camera.position.z < -2:
		camera.position.z = -2

	screen.fill((0, 0, 0))
	#camera.rotation.y = math.sin(time.time_ns() / 1_000_000_000 / 2.0) * 45.0
	hai += 1
	hai = math.fmod(hai, 360)
	render_calls = 0
	draw_box(
		engine.Vector3(0, math.sin(time.time_ns() / 1_000_000_000 * 2.0) / 2.0, 0),
		engine.Vector3(1, abs(math.sin(time.time_ns() / 1_000_000_000.0)), 1),
		engine.Vector3(0, hai, 0),
		engine.Vector3(0, 0, 0)
	)
	draw_box(
		engine.Vector3(0, -1, 0),
		engine.Vector3(2, 1, 2)
	)

	for x in range(-2, 3):
		for z in range(-2, 3):
			draw_box(
				engine.Vector3(x, -2.5, z),
				engine.Vector3(1, 0.5, 1)
			)
	import copy
	cam_rot = copy.copy(camera.rotation)
	cam_rot.y = -cam_rot.y
	cam_rot.x = -cam_rot.x
	cam_pos = copy.copy(camera.position)
	cam_pos.x += math.cos(math.radians(cam_rot.y)) * 0.5
	cam_pos.z -= math.sin(math.radians(cam_rot.y)) * 0.5
	cam_pos.y -= math.cos(math.radians(cam_rot.x)) * 0.5
	draw_box(
		cam_pos,
		engine.Vector3(0.25, 0.25, 1),
		cam_rot
	)
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
	text = font.render("Render calls: " + str(render_calls), False, "white", "black")
	screen.blit(text, pygame.Vector2(0, 16))
	pygame.display.flip()
	clock.tick(30)

pygame.quit()