import pandas as pd
import numpy as np
import math
from PIL import Image

### Classes for Simple Ray Tracer

class ray:
	def __init__(self, x,y,z,v_x,v_y,v_z):
		self.x = x
		self.y = y
		self.z = z
		self.v_x = v_x
		self.v_y = v_y
		self.v_z = v_z

# Light Source Object (Omni-Directional Point Light Source)
# Properties:
#	1.) red: 		RGB red Value between 0 and 255
#	2.) green: 		RGB green Value between 0 and 255
#	3.) blue: 		RGB blue Value between 0 and 255
#	4.) intensity:	Light Intensity between 0 and 1
#	5.) x:			X Coordinate for the light source location
#	6.) y:			Y Coordinate for the light source location
#	7.) z:			Z Coordinate for the light source location

class lightsource:
	def __init__(self, red, green, blue, intensity, x, y, z):
		self.red = red
		self.green = green
		self.blue = blue
		self.intensity = intensity
		self.x = x
		self.y = y
		self.z = z

# Sphere Object
# Properties:
#	1.) radius: 	RGB red Value between 0 and 255
#	2.) x:			X Coordinate for the Sphere
#	3.) y:			Y Coordinate for the Sphere
#	4.) z:			Z Coordinate for the Sphere
#	5.) emissivity:	Emissivity of the surface of the sphere, value between 0 and 1

class sphere:
	def __init__(self, radius, x, y, z, emissivity, name):
		self.radius = radius
		self.x = x
		self.y = y
		self.z = z
		self.emissivity = emissivity
		self.name = name
		
	def intersection(self, vector, origin):
		#Need to define intersection logic for a sphere, only return closest
		
		camera_vector = vector
		camera_origin = origin
		sphere_origin = (self.x, self.y, self.z)
		# Determine Intersection Point of camera_vector and sphere
		dist_intersect_1 = (-(np.dot(camera_vector,(camera_origin-sphere_origin))) + math.sqrt(np.square(np.dot(camera_vector,(camera_origin-sphere_origin))) - (np.linalg.norm(camera_origin - sphere_origin) ** 2) + (self.radius ** 2)))
		dist_intersect_2 = (-(np.dot(camera_vector,(camera_origin-sphere_origin))) - math.sqrt(np.square(np.dot(camera_vector,(camera_origin-sphere_origin))) - (np.linalg.norm(camera_origin - sphere_origin) ** 2) + (self.radius ** 2)))
		#dist_intersect_final = min(dist_intersect_1, dist_intersect_2)
		dist_intersect_final = dist_intersect_2
		#print dist_intersect_1, dist_intersect_2, dist_intersect_final
		intersect_location = dist_intersect_final * camera_vector + camera_origin
		
		return intersect_location
	
	def reflection(self, vector, origin):
	
		#Return ray object reflected off sphere
		sphere_origin = (self.x, self.y, self.z)
		sphere_normal = sphere_normal / np.linalg.norm(sphere_normal)
		reflection = vector - (2 *(np.dot(vector, sphere_normal)) * sphere_normal)
		
		return ray(reflection[0],reflection[1],reflection[2])
		
	
	def does_intersect(self, vector, origin):
	
		#Need to define reflection logic for a 
		
		camera_vector = vector
		camera_origin = origin
		sphere_origin = (self.x, self.y, self.z)
		
		t_0 = np.dot(camera_vector,(sphere_origin - camera_origin))/(np.dot(camera_vector,camera_vector))
		sphere_distance = sphere_origin - (camera_origin + t_0 * camera_vector)
		sphere_distance_mag = np.linalg.norm(sphere_distance)
		
		if sphere_distance_mag <= self.radius:
			return 1
		else:
			return 2
		
# Capture Plane
# Properties:
#	1.) x:					X Coordinate for the center of the capture plane
#	2.) y:					Y Coordinate for the center of the capture plane
#	3.) z:					Z Coordinate for the center of the capture plane
#	4.) width:				Width of the capture plane
#	5.) height:				Height of the capture plane
#	6.) linearpixeldensity:	Linear Pixels per one-unit length
#	7.) camvx		X Component of Camera Vector
#	7.) camvy		Y Component of Camera Vector
#	7.) camvx		Z Component of Camera Vector

class plane:
	def __init__(self, x, y, z, xnorm, ynorm, znorm, emissivity, name) :
		self.x = x
		self.y = y
		self.z = z
		self.xnorm = xnorm
		self.ynorm = ynorm
		self.znorm = znorm
		self.emissivity = emissivity
		self.name = name
	
	def intersection(self, vector, origin):
		#Need to define intersection logic for a plane against
		pass
	
	def reflection(self, vector, origin):
		#Need to define reflection logic for a plane against
		pass
		
		#Return ray object
	
	def does_intersect(self, vector, origin):
		#Need to define reflection logic for a plane against
		pass

class captureplane:
	def __init__(self, x, y, z, width, height, linearpixeldensity, camvx, camvy, camvz) :
		self.x = x
		self.y = y
		self.z = z
		self.width = width
		self.height = height
		self.linearpixeldensity = linearpixeldensity
		self.camvx = camvx
		self.camvy = camvy
		self.camvz = camvz
		
	def get_origin(self):
		return (x,y,z)
	
	def get_vector(self):
		return (camvx, camvy, camvz)
		
class intersection:
	def __init__(self, location, objname):
		self.location = location
		self.objname = objname
	
	#Find distance from give point and intersection
	def distance(self, point):
		pass
		
	def get_origin(self):
		return (x,y,z)
	
	def get_vector(self):
		return (v_x, v_y, v_z)
	
def get_value(capture_get_origin, capture_get_vector, models, lights, iterations):
	# Find Intersection Points For each Object and Camera Ray
		
	#Initialize intersection list
	intersections = []
	
	#Initialize val
	val = 0
		
	# Find camera / object intersections for each object
	num_intersect = 0
	for obj in models:
		# If the Object intersects, then find intersection point(s)
		if obj.does_intersect(capture_get_vector, capture_get_origin):
			intersections.append(obj.intersection(capture_get_vector, capture_get_origin),obj.name)
			num_intersect = num_intersect + 1
		
	if num_intersect > 0:
		
		# Find closest intersection	
		i = 0
		cache_ind = 0
		min_distance = intersections[0].distance(capture_get_origin)
		for obj in intersections:
			if obj.distance(capture_get_origin) < min_distance:
				cache_ind = i
			i = i + 1
			
		closest_intersection = intersections[i]
			
		# Get the found object
		for obj in models:
			if obj.name == closest_intersection.objname:
				intersection_obj = obj
			
		# Need to still loop through the lights and find the resulting value from the found obj/intersection
		for obj in lights:
			# Reflect each light off the object
				
			# Determine the Dot Product
				
			# Get the Resulting Value
			val = 0
		
		# Get the camera reflected values
		# For first iteration setup the reflection from the camera
		capture_reflect = intersection_obj.reflection(capture.get_vector, capture.get_origin)
		
		#Check if there are reflections, if so call get_value again with the new vector
		if iterations > 0:
			#Get the reflected camera array
			capture_reflect = intersection_obj.reflection(capture_get_vector, capture_get_origin)
			#Get the value from the reflected camera array
			val = val + get_value(capture_reflect.get_origin, capture_reflect.get_vector, models, lights, iterations - 1)
	
	return val
		
# Initialize Models & Lighting object lists		
models = []
lights = []
		
# Define Models
models.append(sphere(2.0,3.0,10.0,0.0,1.0,"S1"))
models.append(sphere(2.0,-3.0,10.0,0.0,1.0,"S2"))
# models.append(plane(0.0,0.0,0.0,0.0,0.0,1.0,1.0,"P1"))

# Define Lighting
lights.append(lightsource(100.0,200.0,255.0,1.0,-2.1,0.1,5.0))
lights.append(lightsource(100.0,255.0,200.0,1.0,2.1,-0.1,5.0))

# Define Capture Plane / Camera
capture = captureplane(0.0,0.0,0.0, 10.0, 10.0, 10.0, 0.0, 1.0, 0.0)

# Define Number of Reflections
num_reflect = 1

####### Main Routine ########

# Initialize Image
img = np.zeros((capture.width * capture.linearpixeldensity + 1, capture.height * capture.linearpixeldensity + 1,3),'uint8')

### I know I need to optimize the iteration with pandas/numpy iterators, will get working first...

for row in xrange(0, img.shape[0]):

	# Progress in 5% intervals (assuming width = height)
	if row % round((capture.width * capture.linearpixeldensity + 1)/10) == 0:
		print (row /(capture.width * capture.linearpixeldensity + 1)*100), "% Complete"
		
	for col in xrange(0, img.shape[1]):
		
		# Get the first value
		val = get_value(capture.get_origin, capture.get_vector, models, lights, num_reflect)
