import pandas as pd
import numpy as np
import math
from PIL import Image

### Classes for Simple Ray Tracer

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
		pass
	
	def reflection(self, vector, origin):
		#Need to define reflection logic for a sphere
		pass
		
		#Return ray object
	
	def does_intersect(self, vector, origin):
		#Need to define reflection logic for a sphere
		pass
		
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
		
class intersection(self):
	def __init__(self, location, objname):
		self.location = location
		self.objname = objname
	
	#Find distance from give point and intersection
	def distance(self, point):
		pass
		
class ray(self):
	def __init__(self, x,y,z,v_x,v_y,v_z):
		self.x = x
		self.y = y
		self.z = z
		self.v_x = v_x
		self.v_y = v_y
		self.v_z = v_z
		
	def get_origin(self):
		return (x,y,z)
	
	def get_vector(self):
		return (v_x, v_y, v_z)
	
def get_value(self, capture_get_origin, capture_get_vector, models, lights):
		# Find Intersection Points For each Object and Camera Ray
		
		#Initialize intersection list
		intersections = []
		
		# Find camera / object intersections for each object
		for obj in models:
			# If the Object intersects, then find intersection point(s)
			if obj.does_intersect(capture_get_vector, capture_get_origin):
				intersections.append(obj.intersection(capture_get_vector, capture_get_origin),obj.name)
		
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
			get_value = 1
		
# Initialize Models & Lighting object lists		
models = []
lights = []
		
# Define Models
models.append(sphere(2.0,3.0,10.0,0.0,1.0,"S1"))
models.append(sphere(2.0,-3.0,10.0,0.0,1.0,"S2"))
models.append(plane(0.0,0.0,0.0,0.0,0.0,1.0,1.0,"P1"))

# Define Lighting
lights.append(lightsource(100.0,200.0,255.0,1.0,-2.1,0.1,5.0))
lights.append(lightsource(100.0,255.0,200.0,1.0,2.1,-0.1,5.0))

# Define Capture Plane / Camera
capture = captureplane(0.0,0.0,0.0, 10.0, 10.0, 10.0, 0.0, 1.0, 0.0)

# Define Number of Reflections
num_reflect = 1

####### Main Routine ########

# Initialize Image
img = np.zeros((image_one.width * image_one.linearpixeldensity + 1, image_one.height * image_one.linearpixeldensity + 1,3),'uint8')

### I know I need to optimize the iteration with pandas/numpy iterators, will get working first...

for row in xrange(0, img.shape[0]):

	# Progress in 5% intervals (assuming width = height)
	if row % round((image_one.width * image_one.linearpixeldensity + 1)/10) == 0:
		print (row /(image_one.width * image_one.linearpixeldensity + 1)*100), "% Complete"
		
	for col in xrange(0, img.shape[1]):
		
		# Get the first value
		val = get_value(self, capture.get_origin, capture.get_vector, models, lights)
		
		# Get the camera reflected values
		# For first iteration setup the reflection from the camera
		capture_reflect = intersection_obj.reflection(capture.get_vector, capture.get_origin)
		
		#Loop through each reflection
		for ref_iter in xrange(0, num_reflect - 1)
			val = get_value(self, capture_reflect.get_origin, capture_reflect.get_vector, models, lights)
			capture_reflect = intersection_obj.reflection(capture_reflect.get_vector, capture_reflect.get_origin)
