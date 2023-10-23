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

def rotate_vector3(vector3: Vector3 = Vector3(), rotation: Vector3 = Vector3(), pivot: Vector3 = Vector3(), offset: Vector3 = Vector3()):
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