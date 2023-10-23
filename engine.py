import math

# Change for ESP32
import pygame

def clamp(n, min, max): 
	if n < min: 
		return min
	elif n > max: 
		return max
	else: 
		return n 

class Vector2:
	x: float = 0
	y: float = 0
	def __init__(self, x: float = 0, y: float = 0) -> None:
		self.x = x
		self.y = y
	def __str__(self) -> str:
		return "<Vector3(x: {}, y: {})>".format(str(self.x), str(self.y))
	def __repr__(self) -> str:
		return self.__str__()

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
	min_clipping: float = 0.1
	def __init__(self, position: Vector3 = Vector3(), rotation: Vector3 = Vector3(), fov: float = 90, min_clipping: float = 0.1) -> None:
		self.position = position
		self.rotation = rotation
		self.fov = fov
		self.min_clipping = min_clipping
	def clipping(self, vector3: Vector3) -> Vector3:
		return vector3.z - self.position.z < self.min_clipping
	def __str__(self) -> str:
		return "<Camera(position: {}, rotation: {}, fov: {}, min_clipping: {})".format(str(self.position), str(self.rotation), str(self.fov), str(self.min_clipping))
	def __repr__(self) -> str:
		return self.__str__()

camera: Camera = None

def set_camera(new_camera: Camera = Camera()) -> Camera:
	global camera
	camera = new_camera
	return camera

def new_camera() -> Camera:
	return set_camera()

def add_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3()) -> Vector3:
	return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)

def subtract_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3()) -> Vector3:
	return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)

def multiply_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3()) -> Vector3:
	return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)

def divide_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3()) -> Vector3:
	return Vector3(
		(a.x / b.x) if not a.x == 0 and b.x == 0 else 0,
		(a.y / b.y) if not a.y == 0 and b.y == 0 else 0,
		(a.z / b.z) if not a.z == 0 and b.z == 0 else 0
	)

def lerp_vector3(a: Vector3 = Vector3(), b: Vector3 = Vector3(), t: float = 0.5) -> Vector3:
	return add_vector3(
		a,
		multiply_vector3(
			Vector3(t, t, t),
			subtract_vector3(
				b,
				a
			)
		)
	)

def vector3_distance(a: Vector3 = Vector3(), b: Vector3 = Vector3()) -> float:
    dx = b.x - a.x
    dy = b.y - a.y
    dz = b.z - a.z
    return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

def rotate_vector3(vector3: Vector3 = Vector3(), rotation: Vector3 = Vector3(), pivot: Vector3 = Vector3(), offset: Vector3 = Vector3()) -> Vector3:
	vector3 = subtract_vector3(vector3, pivot)
	
	sine_x = math.sin(math.radians(rotation.x))
	cosine_x = math.cos(math.radians(rotation.x))
	sine_y = math.sin(math.radians(rotation.y))
	cosine_y = math.cos(math.radians(rotation.y))
	sine_z = math.sin(math.radians(rotation.z))
	cosine_z = math.cos(math.radians(rotation.z))
	
	vector3 = Vector3(
		vector3.z * sine_y + vector3.x * cosine_y,
		vector3.y,
		vector3.z * cosine_y - vector3.x * sine_y
	)

	vector3 = Vector3(
		vector3.x,
		vector3.y * cosine_x - vector3.z * sine_x,
		vector3.y * sine_x + vector3.z * cosine_x
	)

	vector3 = Vector3(
		vector3.x * cosine_z - vector3.y * sine_z,
		vector3.x * sine_z + vector3.y * cosine_z,
		vector3.z
	)

	return add_vector3(add_vector3(vector3, pivot), offset)

# Change for ESP32
def center_x(x: float = 0) -> float:
	return x + screen.get_width() / 2.0

# Change for ESP32
def center_y(y: float = 0) -> float:
	return y + screen.get_height() / 2.0

def center_xy(x: float = 0, y: float = 0) -> float:
	return (center_x(x), center_y(y))

# Change for ESP32
def center_screen_vector2(vector2: pygame.Vector2 = pygame.Vector2()) -> pygame.Vector2:
	return pygame.Vector2(center_x(vector2.x), center_y(vector2.y))

# Change for ESP32
def vector3_to_screen_vector2(vector3: Vector3 = Vector3()) -> pygame.Vector2:
	z = vector3.z - camera.position.z
	if z < 0:
		vector3 = Vector3(
			-vector3.x,
			-vector3.y,
			-vector3.z
		)
		z = vector3.z - camera.position.z
	return center_screen_vector2(pygame.Vector2(
		((vector3.x - camera.position.x) / z) if z != 0 else 0,
		(-(vector3.y - camera.position.y) / z) if z != 0 else 0
	) / (camera.fov / 10_000))

# Change for ESP32
def vector2_outside_screen(vector2: pygame.Vector2 = pygame.Vector2()) -> bool:
	x_less = vector2.x < 0
	x_greater = vector2.x > screen.get_width() - 1
	y_less = vector2.y < 0
	y_greater = vector2.y > screen.get_height() - 1
	return x_less or x_greater or y_less or y_greater

draw_list = []
draw_calls = 0

def clear_draw() -> None:
	global draw_list, draw_calls
	draw_list = []
	draw_calls = 0

def draw(list_to_draw: list = None) -> None:
	global draw_calls

	if list_to_draw == None:
		list_to_draw = draw_list

	sorted_list = []
	for info in list_to_draw:
		from_position = info[2]
		to_position = info[3]

		center_position = lerp_vector3(from_position, to_position)
		camera_distance = vector3_distance(center_position, camera.position)
		
		info = list(info)
		info.insert(0, camera_distance)
		info = tuple(info)

		sorted_list.append(info)
	
	sorted_list = sorted(sorted_list, key=lambda x: x[0], reverse=True)
	for info in sorted_list:
		distance = info[0]
		from_vector2 = info[1]
		to_vector2 = info[2]
		color = info[5]
		outline_size = info[6]

		pygame.draw.line(screen, color, from_vector2, to_vector2, round(clamp((1.0 / distance) * (outline_size * 2), 1, 10)))
		draw_calls += 1


# Change for ESP32
def draw_line(from_position: Vector3 = Vector3(), to_position: Vector3 = Vector3(), from_offset: Vector3 = Vector3(), to_offset: Vector3 = Vector3(), rotation: Vector3 = Vector3(), rotation_pivot: Vector3 = Vector3(), color: tuple = (255, 255, 255), outline_size: float = 1) -> pygame.Vector2:
	from_pos = rotate_vector3(
	 	from_position,
		rotation,
		rotation_pivot,
		from_offset
	)
	from_pos = rotate_vector3(
	 	from_pos,
		camera.rotation,
		camera.position
	)

	to_pos = rotate_vector3(
	 	to_position,
		rotation,
		rotation_pivot,
		to_offset
	)
	to_pos = rotate_vector3(
	 	to_pos,
		camera.rotation,
		camera.position
	)

	from_clipping = camera.clipping(from_pos)
	center_clipping = camera.clipping(lerp_vector3(from_pos, to_pos))
	to_clipping = camera.clipping(to_pos)

	if from_clipping and center_clipping and to_clipping:
		return to_position, to_offset

	if from_clipping or to_clipping:
		if from_clipping:
			position = from_position
		else:
			position = to_position
		clipping_amount = abs(position.z - camera.position.z)
		
		new_position = Vector3(
			position.x,
			position.y,
			position.z - clipping_amount
		)

		if from_clipping:
			from_position = new_position
		else:
			to_position = new_position

	from_vector2 = vector3_to_screen_vector2(from_pos)
	to_vector2 = vector3_to_screen_vector2(to_pos)

	if vector2_outside_screen(from_vector2) and vector2_outside_screen(pygame.math.Vector2.lerp(from_vector2, to_vector2, 0.5)) and vector2_outside_screen(to_vector2):
		return to_position, to_offset
	
	global draw_list
	draw_list.append((from_vector2, to_vector2, from_pos, to_pos, color, outline_size))
	return to_position, to_offset

def draw_box(position: Vector3 = Vector3(), size: Vector3 = Vector3(1, 1, 1), rotation: Vector3 = Vector3(), rotation_pivot: Vector3 = Vector3(), color: tuple = (255, 255, 255), outline_size: float = 1) -> None:
	last_position, last_offset = draw_line(
		Vector3(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		Vector3(size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		Vector3(size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		Vector3(-size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		Vector3(-size.x / 2.0, size.y / -2.0, -size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		Vector3(-size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		Vector3(size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		Vector3(-size.x / 2.0, size.y / 2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		last_position,
		Vector3(-size.x / 2.0, size.y / -2.0, size.z / 2.0),
		last_offset,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		Vector3(-size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		Vector3(-size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		Vector3(size.x / 2.0, -size.y / 2.0, -size.z / 2.0),
		Vector3(size.x / 2.0, -size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		Vector3(size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		Vector3(size.x / 2.0, size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

	last_position, last_offset = draw_line(
		Vector3(-size.x / 2.0, size.y / 2.0, -size.z / 2.0),
		Vector3(-size.x / 2.0, size.y / 2.0, size.z / 2.0),
		position,
		position,
		rotation, rotation_pivot, color, outline_size
	)

# PyGame related code

screen: pygame.Surface = None
esp32: bool = True
sort_draw: bool = True

def set_pygame_screen(pygame_screen: pygame.Surface) -> pygame.Surface:
	global screen
	screen = pygame_screen
	return screen