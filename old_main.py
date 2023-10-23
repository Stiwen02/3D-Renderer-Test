import pygame
import old_engine as engine
import math
import time
import os

os.system("@echo off")
os.system("clear")

pygame.init()
screen = pygame.display.set_mode((160, 128))
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

def draw_line(from_position: engine.Vector3 = engine.Vector3(), to_position: engine.Vector3 = engine.Vector3(), from_offset: engine.Vector3 = engine.Vector3(), to_offset: engine.Vector3 = engine.Vector3(), rotation: engine.Vector3 = engine.Vector3(), rotation_pivot: engine.Vector3 = engine.Vector3()) -> pygame.Vector2:
	from_vector2 = vector3_to_pygame(
		engine.add_vector3(
			engine.rotate_vector3(
				from_position,
				engine.subtract_vector3(
					rotation,
					camera.rotation
				),
				rotation_pivot
			),
			from_offset
		)
	)
	to_vector2 = vector3_to_pygame(
		engine.add_vector3(
			engine.rotate_vector3(
				to_position,
				engine.subtract_vector3(
					rotation,
					camera.rotation
				),
				rotation_pivot
			),
			to_offset
		)
	)
	
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

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEMOTION:
			dx, dy = event.rel
			camera.rotation.y += dx
			camera.rotation.x += dy
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	screen.fill((0, 0, 0))
	#camera.rotation.x = math.sin(time.time_ns() / 1_000_000_000 / 2.0) * 45.0
	hai += 1
	hai = math.fmod(hai, 360)
	draw_box(
		engine.Vector3(0, math.sin(time.time_ns() / 1_000_000_000 * 2.0) / 2.0, 0),
		engine.Vector3(1, abs(math.sin(time.time_ns() / 1_000_000_000.0)), 1),
		engine.Vector3(0, hai, hai)
	)
	draw_box(
		engine.Vector3(0, -1, 0),
		engine.Vector3(2, 1, 2),
		engine.Vector3(0, 0, 0),
		engine.Vector3(0, 0, 0)
	)

	pygame.display.flip()
	clock.tick(30)

pygame.quit()