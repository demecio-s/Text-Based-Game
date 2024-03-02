import numpy as np
import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, faceX, faceY, faceZ): #defines the first 3 planes of faces
        self.z = faceZ
        self.y = faceY
        self.x = faceX
        
    def bounds(self, x, y, z, xbool, ybool, zbool): 
        if xbool:
            xbounds = np.array([self.x - x, self.x])
        else:
            xbounds = x
            
        if ybool:
            ybounds = np.array([self.y - y, self.y])
        else: 
            ybounds = y
            
        if zbool:
            zbounds = np.array([self.z - z, self.z])
        else:
            zbounds = z
            
        return [xbounds, ybounds, zbounds]
    
    def color(self, ambient, diffuse, specular, shine, reflection):
        if type(ambient) != np.ndarray or type(diffuse) != np.ndarray or type(specular) != np.ndarray:
            print('make sure to use correct type of stuff')
            return None
        else:
            return ambient, diffuse, specular, shine, reflection
    

def normalize(vector):
    return vector / np.linalg.norm(vector)

def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def intersect(ray_origin, direction_vector, check_coord, axis_number, x_range, y_range, z_range):
    axis_number -= 1    
    ranges = [x_range, y_range, z_range]
    t = np.linspace(0, 5, 100) ### might need to correct these bounds 
    accuracy = (max(t)-min(t))/len(t)
    tvals = []
    tval = None
    for i in range(len(t)):
        v = ray_origin + direction_vector * t[i]
        if abs(v[axis_number] - check_coord) <= accuracy:
            for j in range(len(ranges)):
                if type(ranges[j]) == np.ndarray:
                    if v[j] <= max(ranges[j]) and v[j] >= min(ranges[j]):
                        tval = t[i]
                    else:
                        tval = None
                        break
        if tval != None:
            tvals.append(tval)

    l = np.mean(tvals)
    if np.isnan(l):
        return None
    else:

        return l


def nearest_intersected_object(objects, ray_origin, direction_vector, check_coord, axis_number):
    distances = []
    intersection = intersect(ray_origin, direction_vector, check_coord, axis_number, objects[0], objects[1], objects[2])
    if intersection != None:
        distances.append(intersection)
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects 
    return nearest_object, min_distance

width = 100
height = width

max_depth = 3

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio) # left top right bottom

light = { 'position': np.array([1, 1, 1]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1]) }

############################ KEY KEY KEY KEY KEY #############################
#                 key handle               key stem(spine)         tooth                       tooth                       lil square
key_parts = [Rectangle(7/6, 1/3, -1), Rectangle(1/2, 1/6, -1), Rectangle(-5/6, -1/6, -1), Rectangle(-1/2, -1/6, -1), Rectangle(-2/3, -1/6, -1)]
key = [key_parts[0].bounds(2*(1/3), 2*(1/3), -1, True, True, False), key_parts[1].bounds(5/3, 1/3, -1, True, True, False), key_parts[2].bounds(1/6, 1/3, -1, True, True, False),  key_parts[3].bounds(1/6, 1/3, -1, True, True, False), key_parts[4].bounds(1/6, 1/6, -1, True, True, False)]

key_color = []
for part in range(len(key_parts)):  
    key_color.append(key_parts[part].color(np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 1]), 100, 0.5))

########################### SWORD SWORD SWORD ###############################
#                 grip                       vertical thingy           blade
sword_parts = [Rectangle(7/6, 1/12, -1), Rectangle(5/6, 1/2, -1), Rectangle(2/3, 1/6, -1)]
sword = [sword_parts[0].bounds(1/3, 1/6, -1, True, True, False), sword_parts[1].bounds(1/6, 1, -1, True, True, False), sword_parts[2].bounds(7/6, 1/3, -1, True, True, False)]

# tip
maxim = 1/6
yinc = 1/42
l = 2
for j in reversed(np.linspace(-7/6, -1/2, 7)):
    maxim -= yinc
    minim = 2* maxim
    l += 1
    sword_parts.append(Rectangle(j, maxim, -1))
    sword.append(sword_parts[l].bounds(2/21, minim, -1, True, True, False))

sword_color = [sword_parts[0].color(np.array([0.3961, 0.2627, 0.1294]), np.array([0.3961, 0.2627, 0.1294]), np.array([0, 0, 0]), 0, 0.25), sword_parts[1].color(np.array([0.1, 0.1, 0.1]), np.array([0.1, 0.1, 0.1]), np.array([1, 1, 1]), 100, 0.5),  sword_parts[2].color(np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1, 1, 1]), 100, 0.5)]

l = 3
for i in range(7):  
    sword_color.append(sword_parts[l].color(np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1-0.8275, 1-0.8275, 1-0.8275]), np.array([1, 1, 1]), 100, 0.5))
    l+=1


objects = sword
colors = sword_color
image = np.zeros((height, width, 3))
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)
        color = np.zeros((3))
        reflection = 1
        for part in range(len(objects)):
            for k in range(max_depth):

                ## Checks for ray intersection at nearest object
                nearest_object, min_distance = nearest_intersected_object(objects[part], origin, direction, -1, 3) 
    
                if nearest_object is None:
                    break
                intersection = np.array(origin + min_distance * direction)
                
                ## prepares new ray origin close to intersection in direction of 
                for h in range(len(nearest_object)):
                    if type(nearest_object[h]) != np.ndarray:
                        diff = np.copy(intersection) 
                        diff[h] = intersection[h]-1
                        break
                normal_to_surface = normalize(intersection - diff)

                shifted_point = intersection + 1e-5 * normal_to_surface
                intersection_to_light = normalize(light['position'] - shifted_point) ## direction to light
            
                ## Color gets calculated after this point
                illumination = np.zeros((3))
    
                # ambient
                if objects[part] == nearest_object:
                    illumination += colors[part][0] * light['ambient']
    
                    # diffuse
                    illumination += colors[part][1] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)
    
                    # specular
                    intersection_to_camera = normalize(camera - intersection)
                    H = normalize(intersection_to_light + intersection_to_camera)
                    illumination += colors[part][2] * light['specular'] * np.dot(normal_to_surface, H) ** (colors[part][3] / 4)
    
                    # reflection
                    color += reflection * illumination
                    reflection *= colors[part][4]
                    # print(color)
                    # input()
                    origin = shifted_point
                    direction = reflected(direction, normal_to_surface)

        image[i, j] = np.clip(color, 0, 1)

plt.imsave('image.pdf', image)
print('all done!')