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
		
		camera_vector = np.array(vector)
		camera_origin = np.array(origin)
		sphere_origin = np.array((self.x, self.y, self.z))
 
		# Determine Intersection Point of camera_vector and sphere
		dist_intersect_1 = (-(np.dot(camera_vector,(camera_origin-sphere_origin))) + math.sqrt(np.square(np.dot(camera_vector,(camera_origin-sphere_origin))) - (np.linalg.norm(camera_origin - sphere_origin) ** 2) + (self.radius ** 2)))
		dist_intersect_2 = (-(np.dot(camera_vector,(camera_origin-sphere_origin))) - math.sqrt(np.square(np.dot(camera_vector,(camera_origin-sphere_origin))) - (np.linalg.norm(camera_origin - sphere_origin) ** 2) + (self.radius ** 2)))
		#dist_intersect_final = min(dist_intersect_1, dist_intersect_2)
		dist_intersect_final = dist_intersect_2
		#print dist_intersect_1, dist_intersect_2, dist_intersect_final
		intersect_location = dist_intersect_final * camera_vector + camera_origin

		return intersect_location
	
	def reflection(self, vector, origin, intersection):
	
		#Return ray object reflected off sphere
		vector = np.array(vector)
		sphere_origin = (self.x, self.y, self.z)
		sphere_normal = list(np.array(intersection) - np.array(sphere_origin))
		sphere_normal = sphere_normal / np.linalg.norm(sphere_normal)
		reflection = vector - 2 * ((np.dot(vector, sphere_normal)) * sphere_normal)
		
		return ray(intersection[0],intersection[1],intersection[2],reflection[0],reflection[1],reflection[2])
	
	def does_intersect(self, vector, origin):
	
		#Need to define reflection logic for a 
		
		camera_vector = vector
		camera_origin = origin
		sphere_origin = (self.x, self.y, self.z)

		t_0 = np.dot(camera_vector,((np.array(sphere_origin)-np.array(camera_origin))))/(np.dot(camera_vector,camera_vector))
		sphere_distance = np.array(sphere_origin) - (np.array(camera_origin) + t_0 * np.array(camera_vector))
		sphere_distance_mag = np.linalg.norm(sphere_distance)
		
		if sphere_distance_mag <= self.radius:
			return 1
		else:
			return 0
		
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
		return (self.x,self.y,self.z)
	
	def get_vector(self):
		return (self.camvx, self.camvy, self.camvz)
		
class intersection:
	def __init__(self, location, objname):
		self.location = location
		self.objname = objname
	
	#Find distance from give point and intersection
	def distance(self, point):
		return np.linalg.norm(np.array(self.location) - np.array(point))
	
def get_value(capture_get_origin, capture_get_vector, models, lights, iterations):
	# Find Intersection Points For each Object and Camera Ray
		
	#Initialize intersection list
	intersections = []
	
	#Initialize val
	val = np.array([0.0,0.0,0.0])
		
	# Find camera / object intersections for each object
	num_intersect = 0
	for obj in models:
		# If the Object intersects, then find intersection point(s)
		if obj.does_intersect(capture_get_vector, capture_get_origin):
		
			intersection_point = obj.intersection(capture_get_vector, capture_get_origin)
			intersections.append(intersection(intersection_point, obj.name))

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
			
		closest_intersection = intersections[cache_ind]
			
		# Get the found object
		for obj in models:
			if obj.name == closest_intersection.objname:
				intersection_obj = obj
			
		# Need to still loop through the lights and find the resulting value from the found obj/intersection
		val = np.array([0.0,0.0,0.0])
		for obj in lights:
			
			# Reflect each light off the object
			light_origin = np.array([obj.x, obj.y, obj.z])
			light_vector = np.array(closest_intersection.location) - list(np.array(light_origin))
			light_vector = light_vector / np.linalg.norm(light_vector)
			
			#Determine if light is visible
			#First get closest intersection
			light_intersection = intersection_obj.intersection(light_vector, light_origin)
			
			#Then determine if closest intersection is the same intersection closest to camera
			if abs(np.linalg.norm(light_intersection - np.array(closest_intersection.location))) < .001:
				#If it is the same, do all the calculations
				light_reflection = intersection_obj.reflection(light_vector, light_origin, closest_intersection.location)
				light_reflection_vector = np.array([light_reflection.v_x, light_reflection.v_y, light_reflection.v_z])
				#print light_reflection_vector, light_vector, closest_intersection.location
				
				#print capture_get_vector
				# Determine the light intensity
				light_intensity = np.dot(np.array(light_reflection_vector), -np.array(capture_get_vector))* intersection_obj.emissivity * obj.intensity
				#print capture_get_vector, light_reflection_vector, light_vector, closest_intersection.location, light_intensity
				
				k = 0.1 #Constant to the exponential equation for scaling the output of the light/camera dot product
				light_intensity = k * (((math.sqrt(4 * (k ** 2) + 1)+1)/(2 * k)) ** light_intensity) - k /(((math.sqrt(4 * (k ** 2) + 1)+1)/(2 * k)))
				
				
				total_intensity = light_intensity + 0.3
				
				if total_intensity > 1:
					total_intensity = 1.0
				#total_intensity = 0.3
				#val = np.array([total_intensity * obj.red,total_intensity * obj.green,total_intensity * obj.blue])
				val = np.array(val) + np.array([total_intensity * obj.red,total_intensity * obj.green,total_intensity * obj.blue])
			else:
				#Otherwise just add 0.1 for ambient lighting
				total_intensity = 0.3
				val = np.array(val) + np.array([total_intensity * obj.red,total_intensity * obj.green,total_intensity * obj.blue])
			
			#print out the full color values based on total_intensity
		#val = np.array(val) + np.array([total_intensity * obj.red,total_intensity * obj.green,total_intensity * obj.blue])
			#print val
			# Get the Resulting Value
			
		
		# Get the camera reflected values
		# For first iteration setup the reflection from the camera
		capture_reflect = intersection_obj.reflection(capture_get_vector, capture.get_origin(), closest_intersection.location)
		
		#Check if there are reflections, if so recurse on get_value
		if iterations > 0:
			#Get the reflected camera array
			capture_reflect = intersection_obj.reflection(capture_get_vector, capture_get_origin, closest_intersection.location)
			reflect_origin = (capture_reflect.x, capture_reflect.y, capture_reflect.z)
			reflect_vector = (capture_reflect.v_x, capture_reflect.v_y, capture_reflect.v_z)
			#Get the value from the reflected camera array
			
			val = np.array(val) + 0.2 * get_value(reflect_origin, reflect_vector, models, lights, iterations - 1)
			if val[0] > 255.0:
				val[0] = 255.0
			if val[1] > 255.0:
				val[1] = 255.0
			if val[2] > 255.0:
				val[2] = 255.0
	else:
		#Set return value to 0's if no intercept
		val = np.array([0.0,0.0,0.0])
	
	#Return the value
	if val[0] > 255.0:
		val[0] = 255.0
	if val[1] > 255.0:
		val[1] = 255.0
	if val[2] > 255.0:
		val[2] = 255.0
	
	return val
		
# Initialize Models & Lighting object lists		
models = []
lights = []
		
# Define Models
models.append(sphere(1.8547,3.0,10.0,0.0,1.0,"S1"))
models.append(sphere(1.998,-3.0,10.0,0.0,1.0,"S2"))
models.append(sphere(1.978,0.0,10.0,-3.0,1.0,"S3"))
models.append(sphere(1.997,0.0,10.0,3.0,1.0,"S4"))
models.append(sphere(0.8576,0.0,10.0,0.0,1.0,"S5"))
#models.append(plane(0.0,0.0,0.0,0.0,0.0,1.0,1.0,"P1"))

# Define Lighting
lights.append(lightsource(0.0,255.0,0.0,1.0,0.2,0.3,5.1))
lights.append(lightsource(0.0,0.0,255.0,1.0,2.1,0.2,-5.21))
#lights.append(lightsource(150.0,0.0,0.0,1.0,-4.121,0.21,0.11))

# Define Capture Plane / Camera
capture = captureplane(0.0,0.0,0.0, 10.0, 10.0, 100.0, 0.0, 1.0, 0.0)

# Define Number of Reflections
num_reflect = 10

####### Main Routine ########

# Initialize Image
img = np.zeros((capture.width * capture.linearpixeldensity + 1, capture.height * capture.linearpixeldensity + 1,3),'uint8')

### I know I need to optimize the iteration with pandas/numpy iterators, will get working first...

for row in xrange(0, img.shape[0]):

	# Progress in 5% intervals (assuming width = height)
	if row % round((capture.width * capture.linearpixeldensity + 1)/100) == 0:
		print (row /(capture.width * capture.linearpixeldensity + 1)*100), "% Complete"
		
	for col in xrange(0, img.shape[1]):
		camera_origin = np.array([capture.x - capture.width/2 + row / capture.linearpixeldensity, capture.y, capture.z - capture.height/2 + col / capture.linearpixeldensity])

		# Get the value
		#print camera_origin
		img[row,col] = get_value(camera_origin, capture.get_vector(), models, lights, num_reflect)
		img[row,col,0] = min(img[row,col,0],255.0)
		img[row,col,1] = min(img[row,col,1],255.0)
		img[row,col,2] = min(img[row,col,2],255.0)
		
img_file = Image.fromarray(img)
img_file.save('multiple_objects_2.jpeg')
