import  K_means
from image_utils import *

# file = input("image file> ")
file = 'input_images/umn_Willey_Hall-tiny.ppm'

image = read_ppm(file)
###CHANGE
k = 3
#k = int(input("What would you like your 'k' value to be?"))
image = K_means.get_image(image, k)
#may need to return something
save_ppm("k_means.ppm", image)
