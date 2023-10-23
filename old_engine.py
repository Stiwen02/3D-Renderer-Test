import pygame
import math

class Vector3:
	x: float = 0
	y: float = 0
	z: float = 0
	def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
		self.x = x
		self.y = y
		self.z = z
	def __str__(self) -> str:
		return "<Vector3(x: {}, y: {}, z: {})>".format(str(self.x), str(self.y), str(self.z))
	def __repr__(self) -> str:
		return self.__str__()

class Camera:
	position: Vector3 = Vector3()
	rotation: Vector3 = Vector3()
	fov: float = 90
	def __init__(self, position: Vector3 = Vector3(), rotation: Vector3 = Vector3(), fov: float = 90) -> None:
		self.position = position
		self.rotation = rotation
		self.fov = fov
	def __str__(self) -> str:
		return "<Camera(position: {}, rotation: {}, fov: {})".format(str(self.position), str(self.rotation), str(self.fov))
	def __repr__(self) -> str:
		return self.__str__()

camera: Camera = None

def set_camera(new_camera: Camera = Camera()) -> Camera:
	global camera
	camera = new_camera
	return camera

def new_camera() -> Camera:
	return set_camera()

def add_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3()):
	return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)

def subtract_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3()):
	return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)

def rotate_vector3(vector3: Vector3 = Vector3(), rotation: Vector3 = Vector3(), pivot: Vector3 = Vector3()):
	translated_vector = Vector3(vector3.x - pivot.x, vector3.y - pivot.y, vector3.z - pivot.z)
	
	rotation_x = math.radians(rotation.x)
	rotation_y = math.radians(rotation.y)
	rotation_z = math.radians(rotation.z)
	
	rotated_x = translated_vector.x * math.cos(rotation_y) * math.cos(rotation_z) - translated_vector.y * (
			math.cos(rotation_x) * math.sin(rotation_z) - math.sin(rotation_x) * math.sin(rotation_y) * math.cos(
		rotation_z)) + translated_vector.z * (
						math.sin(rotation_x) * math.sin(rotation_z) + math.cos(rotation_x) * math.sin(rotation_y) * math.cos(
					rotation_z))
	rotated_y = translated_vector.x * math.cos(rotation_y) * math.sin(rotation_z) + translated_vector.y * (
			math.cos(rotation_x) * math.cos(rotation_z) + math.sin(rotation_x) * math.sin(rotation_y) * math.sin(
		rotation_z)) - translated_vector.z * (
						math.sin(rotation_x) * math.cos(rotation_z) - math.cos(rotation_x) * math.sin(rotation_y) * math.sin(
					rotation_z))
	rotated_z = -translated_vector.x * math.sin(rotation_y) + translated_vector.y * math.sin(rotation_x) * math.cos(
		rotation_y) + translated_vector.z * math.cos(rotation_x) * math.cos(rotation_y)
	
	rotated_vector = Vector3(rotated_x + pivot.x, rotated_y + pivot.y, rotated_z + pivot.z)
	
	return rotated_vector