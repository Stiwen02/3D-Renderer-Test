import pygame
import engine
import math
import time
import os

os.system("@echo off")
os.system("clear")

engine.esp32 = False
engine.sort_draw = False

pygame.init()
screen = pygame.display.set_mode((160, 128) if engine.esp32 else (160*3, 128*3), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

engine.set_pygame_screen(screen)

camera = engine.new_camera()
camera.position.z = -2

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
font = pygame.font.Font('freesansbold.ttf', 16)

rotation = 0

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

	engine.clear_draw()
	engine.draw_box(
		engine.Vector3(-1.5, 2, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(0, rotation, 0)
	)
	engine.draw_box(
		engine.Vector3(1.5, 2, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(rotation, 0, 0)
	)
	engine.draw_box(
		engine.Vector3(0, 2, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(rotation, rotation, 0)
	)
	engine.draw_box(
		engine.Vector3(-1, 3.5, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(45, rotation, 0)
	)
	engine.draw_box(
		engine.Vector3(1, 3.5, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(rotation, 45, 0)
	)
	engine.draw_box(
		engine.Vector3(0, 5, 0),
		engine.Vector3(1, 1, 1),
		engine.Vector3(0, 0, rotation)
	)
	engine.draw_box(
		engine.Vector3(0, -1, 0),
		engine.Vector3(2, 1, 2),
		outline_size=2
	)
	engine.draw_box(
		engine.Vector3(0, math.sin(time.time_ns() / 1_000_000_000 * 2.0) / 2.0, 0),
		engine.Vector3(1, abs(math.sin(time.time_ns() / 1_000_000_000.0)), 1),
		engine.Vector3(0, rotation, 0),
		engine.Vector3(0, 0, 0),
		(0, 255, 0),
		5
	)
	engine.draw()

	fps = round(clock.get_fps())
	fps_color = "red"
	if fps > 10:
		fps_color = "orange"
		if fps > 20:
			fps_color = "yellow"
			if fps > 25:
				fps_color = "green"
	
	if not engine.esp32:
		text = font.render("FPS: " + str(fps), False, fps_color, "black")
		screen.blit(text, pygame.Vector2(0, 16*0))
		text = font.render("Draw calls: " + str(engine.draw_calls), False, "white", "black")
		screen.blit(text, pygame.Vector2(0, 16*1))
		text = font.render("Draw list length: " + str(len(engine.draw_list)), False, "white", "black")
		screen.blit(text, pygame.Vector2(0, 16*2))
		# text = font.render("Sort draw: " + str(engine.sort_draw), False, "white", "black")
		# screen.blit(text, pygame.Vector2(0, 16*3))

	pygame.display.flip()
	clock.tick(30)

pygame.quit()