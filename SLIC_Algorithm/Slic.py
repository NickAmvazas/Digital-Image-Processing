from matplotlib import image
from matplotlib import pyplot
import math
from numpy import size,mean
import time

class SuperPixel:
  def __init__(self, r, g, b, center_x, center_y,id):
    self.r = r
    self.g = g
    self.b = b
    self.center_x = center_x
    self.center_y = center_y
    self.id = id
    self.group_of_pixels = []

    
def calc_d_c(r_1,g_1,b_1,r_2,g_2,b_2):
    d_c = math.sqrt( math.pow(int(r_1)-int(r_2),2) + math.pow(int(g_1)-int(g_2),2) + math.pow(int(b_1)-int(b_2),2) )
    return d_c

def calc_d_s(x_1,y_1,x_2,y_2,):
    d_s = math.sqrt( math.pow(x_1-x_2,2) + math.pow(y_1-y_2,2) )
    return d_s

def calc_D(d_c,d_s,s,c):
    d = math.sqrt( math.pow(d_c,2) + math.pow(d_s/s,2) * math.pow(c,2) )
    return d

start_time = time.time()

# Load Image as Pixel array
image = image.imread('lena.jpg')

# Set Parameters
#---------------------------------------------
iterations = 5;    
number_of_superpixels = 35;   
c = 1
#---------------------------------------------
number_of_pixels = image.shape[0] * image.shape[1]
s = math.ceil(math.sqrt(number_of_pixels/number_of_superpixels))

print("Image Info:")
print("\tImage Shape: " + format(image.shape))
print("\tTotal number of pixels in image: " + format(number_of_pixels))
print("\tS = " + format(s))

# Create the Image Grid of SuperPixels
#---------------------------------------------
x_array = []
for i in range(round(s/2), image.shape[0], round(s)):
    x_array.append(i)

y_array = []
for j in range(round(s/2), image.shape[1], round(s)):
    y_array.append(j)

id_superPix = 1
image_grid=[]
for x in x_array:
    for y in y_array:
        r= image[x][y][0]
        g= image[x][y][1]
        b= image[x][y][2]        
        superPixel = SuperPixel(r,g,b,x,y,id_superPix)
        image_grid.append(superPixel)
        id_superPix = id_superPix + 1
#---------------------------------------------

"""
# Print x,y for each superPixel
for suppixel in image_grid:
    print(suppixel.id,suppixel.center_x,suppixel.center_y)

"""

"""
# Show the Image Grid of SuperPixels      
for superPixel in image_grid:
   image[superPixel.center_x][superPixel.center_y] = (0,200,10)

# Display Image
pyplot.imshow(image)
pyplot.show()

"""
print("\tTotal number of superPixels: "+format(size(image_grid)))

for i in range(iterations): 
    for x in range(image.shape[0]): 
        for y in range(image.shape[1]): 
            min_dist = math.inf       
            for superPixel in image_grid:
                if math.sqrt(math.pow(x-superPixel.center_x,2) + math.pow(y-superPixel.center_y,2)) < 2*s: # Checking neighborhood of 2s
                    d_c = calc_d_c(image[x][y][0],image[x][y][1],image[x][y][2],superPixel.r,superPixel.g,superPixel.b)
                    d_s = calc_d_s(x,superPixel.center_x,y,superPixel.center_y)
                    D = calc_D(d_c,d_s,s,c)
                    if D < min_dist:
                        min_dist = D
                        superPixel_with_min_distance = superPixel.id
            for superPixel in image_grid:
                if superPixel.id == superPixel_with_min_distance:
                    superPixel.group_of_pixels.append([x,y])
    
    # Calc New Centers for next Iteration
    for superPixel in image_grid:
        new_superPx_center = mean(superPixel.group_of_pixels,axis=0)
        superPixel.center_x = round(new_superPx_center[0])
        superPixel.center_y = round(new_superPx_center[1])
        
        """
        # Print x,y for each superPixel
        print(superPixel.id,superPixel.center_x,superPixel.center_y)
        """

    # Set superPixel color to his children
    for superPixel in image_grid:
        for pixel in superPixel.group_of_pixels:
            image[pixel[0]][pixel[1]][0] = superPixel.r
            image[pixel[0]][pixel[1]][1] = superPixel.g
            image[pixel[0]][pixel[1]][2] = superPixel.b

print("\tProgram Run Time: %s " % (time.time() - start_time))

# Display Image
pyplot.imshow(image)
pyplot.show()