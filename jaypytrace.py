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
	def __init__(self, radius, x, y, z, emissivity):
		self.radius = radius
		self.x = x
		self.y = y
		self.z = z
		self.emissivity = emissivity
		
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

def pixelvalue(row, col, lightsource, sphere, captureplane, color):

	###	Determine Pixel Value
	
	# 1.) Find Closest Sphere / Camera Intersection
	
	# Camera Vector and Starting Point
	camera_vector = np.array([captureplane.camvx, captureplane.camvy, captureplane.camvz])
	# Make camera_vector a unit vector
	camera_vector = camera_vector / np.linalg.norm(camera_vector)
	camera_origin = np.array([captureplane.x - captureplane.width/2 + row / captureplane.linearpixeldensity, captureplane.y, captureplane.z - captureplane.height/2 + col / captureplane.linearpixeldensity])
	
	# Check that Line Intersects Sphere (ensure closest point to ray within radius)
	sphere_origin = np.array([sphere.x, sphere.y, sphere.z])
	t_0 = np.dot(camera_vector,(sphere_origin - camera_origin))/(np.dot(camera_vector,camera_vector))
	sphere_distance = sphere_origin - (camera_origin + t_0 * camera_vector)
	sphere_distance_mag = np.linalg.norm(sphere_distance)
	
	# If minimum distance of sphere to ray is greater than the radius, then return 0
	if sphere_distance_mag >= sphere.radius:
		return 0
	else:
		# Determine Intersection Point of camera_vector and sphere
		dist_intersect_1 = (-(np.dot(camera_vector,(camera_origin-sphere_origin))) + math.sqrt(np.square(np.dot(camera_vector,(camera_origin-sphere_origin))) - (np.linalg.norm(camera_origin - sphere_origin) ** 2) + (sphere.radius ** 2)))
		dist_intersect_2 = (-(np.dot(camera_vector,(camera_origin-sphere_origin))) - math.sqrt(np.square(np.dot(camera_vector,(camera_origin-sphere_origin))) - (np.linalg.norm(camera_origin - sphere_origin) ** 2) + (sphere.radius ** 2)))
		#dist_intersect_final = min(dist_intersect_1, dist_intersect_2)
		dist_intersect_final = dist_intersect_2
		#print dist_intersect_1, dist_intersect_2, dist_intersect_final
		intersect_location = dist_intersect_final * camera_vector + camera_origin
		
		#Next Get the vector from the light source to the intersect location
		light_origin = np.array([lightsource.x, lightsource.y, lightsource.z])
		light_vector = intersect_location - light_origin
		light_vector = light_vector / np.linalg.norm(light_vector)
		
		#Next see if the intersect point is visible to the light source
		dist_intersect_light_1 = (-(np.dot(light_vector,(light_origin-sphere_origin))) + math.sqrt(np.square(np.dot(light_vector,(light_origin-sphere_origin))) - (np.linalg.norm(light_origin - sphere_origin) ** 2) + (sphere.radius ** 2)))
		dist_intersect_light_2 = (-(np.dot(light_vector,(light_origin-sphere_origin))) - math.sqrt(np.square(np.dot(light_vector,(light_origin-sphere_origin))) - (np.linalg.norm(light_origin - sphere_origin) ** 2) + (sphere.radius ** 2)))
		
		dist_light_final = min(dist_intersect_light_1, dist_intersect_light_2)
		light_min_location = dist_light_final * light_vector + light_origin
		
		# If the closest point to the light isn't the point visible to the camera, in shadow
		if abs(np.linalg.norm(light_min_location - intersect_location)) > .001:
			#Include for ambient lighting
			total_intensity = 0.2
			if color == 'red':
				return total_intensity  * lightsource.red
			elif color == 'green':
				return total_intensity * lightsource.green
			elif color == 'blue':
				return total_intensity  * lightsource.blue
			else:
				return 0
		else:
		
			# Light Reflection using Sphere's normal vector
			sphere_normal = sphere_origin - light_min_location
			sphere_normal = sphere_normal / np.linalg.norm(sphere_normal)
			light_reflection = light_vector - (2 *(np.dot(light_vector, sphere_normal)) * sphere_normal)
			light_intensity = np.dot(light_reflection, -camera_vector) * sphere.emissivity * lightsource.intensity
			
			# For the equation y(x) = k*A^x	- b, the light intensity equation will be solved for case where y(-1)=0 and y(1)=1. 
			# I did this exponential equation think to scale a range of -1 through 1, to 0 through 1. From some trial and error I liked a k of 0.05
			k = 0.05 #Constant to the exponential equation for scaling the output of the light/camera dot product
			light_intensity = k * (((math.sqrt(4 * (k ** 2) + 1)+1)/(2 * k)) ** light_intensity) - k /(((math.sqrt(4 * (k ** 2) + 1)+1)/(2 * k)))
			
			#Add for ambient lighting
			total_intensity = light_intensity + 0.2
			
			#In case the ambient lighting puts you over the edge
			if total_intensity > 1:
				total_intensity = 1
			
			
			if color == 'red':
				return total_intensity * lightsource.red
			elif color == 'green':
				return total_intensity * lightsource.green
			elif color == 'blue':
				return total_intensity  * lightsource.blue
			else:
				return 0

### Initialize the first light source, sphere, and capture plane
light_one = lightsource(0.0,0.0,0.0,1.0,-10.2,0.3,10.1)
light_two = lightsource(0.0,0.0,240.0,1.0,10.1,0.1,-10.1)
light_three = lightsource(0.0,240.0,200.0,1.0,-10.1,0.1,10.1)
sphere_one = sphere(4.0,0.0,10.0,0.0,1.0)
image_one = captureplane(0.0,0.0,0.0, 8.0, 8.0, 100.0, 0.0, 1.0, 0.0)

img = np.zeros((image_one.width * image_one.linearpixeldensity + 1, image_one.height * image_one.linearpixeldensity + 1,3),'uint8')
img2 = np.zeros((image_one.width * image_one.linearpixeldensity + 1, image_one.height * image_one.linearpixeldensity + 1,3),'uint8')

### I know I need to optimize the iteration with pandas/numpy iterators, will get working first...
for row in xrange(0, img.shape[0]):
	# Progress in 5% intervals (assuming width = height)
	if row % round((image_one.width * image_one.linearpixeldensity + 1)/200) == 0:
		print (row /(image_one.width * image_one.linearpixeldensity + 1)*100), "% Complete"
		
	for col in xrange(0, img.shape[1]):
		
		# Calculate the image value
		#img[row, col, 1] = pixelvalue_debug2(row, col, light_one, sphere_one, image_one, 'green')
		img[row, col, 0] = min(pixelvalue(row, col, light_one, sphere_one, image_one, 'red') + pixelvalue(row, col, light_two, sphere_one, image_one, 'red') + pixelvalue(row, col, light_three, sphere_one, image_one, 'red'), 255)
		img[row, col, 1] = min(pixelvalue(row, col, light_one, sphere_one, image_one, 'green') + pixelvalue(row, col, light_two, sphere_one, image_one, 'green') + pixelvalue(row, col, light_three, sphere_one, image_one, 'green'), 255)
		img[row, col, 2] = min(pixelvalue(row, col, light_one, sphere_one, image_one, 'blue') + pixelvalue(row, col, light_two, sphere_one, image_one, 'blue') + pixelvalue(row, col, light_three, sphere_one, image_one, 'blue'), 255)
		#print img[row,col,0],img[row,col,1], row, col

img_file = Image.fromarray(img)
img_file.save('sphere_test.jpeg')
