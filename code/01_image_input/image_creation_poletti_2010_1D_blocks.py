import numpy as np
import matplotlib.pyplot as plt
import cv2
from ms_functions import *
import sys

plt.switch_backend('agg')


#IMAGE-CREATION---------------------------------------------------------------------------------------------------------

# from input
suff = sys.argv[1]
fem = sys.argv[2]

print("IMAGE CREATION BLOCKS " + suff)

file_dir = "../../video/img_input/poletti2010/blocks/" + str(suff) + "/"

image_height = 30
# dot size of 4 arcmin -> 8px
radius = 4.
# size border in arcmin -> px = 2 times
border_size = 10.
# velocity is 30 arcmin/s -> 60px/1000ms
velocity = 0.06
# 1s observation time
film_length = 1000
# int(framerate)*(stripe_width+gap)

# for normal distributed FEM
sigma = 0.632

# get normal 2d distribution
# use this to get same statistics as for actual 2D random walk -> use only x-component
mean = [0, 0]
cov = [[1, 0], [0, 1]]
tl_x, tl_y = sigma*np.random.multivariate_normal(mean, cov, film_length).T
rm = tl_x

d_data = open(file_dir + 'displacement.data', 'wb')
np.save(d_data, (tl_x, tl_y))
d_data.close()

f_names = ["dot", "dot_m", "border", "border_m"]

for f_name in f_names:

    print(f_name + " " + suff)

    file_location = file_dir + f_name
    vel = 0

    #set velocity for moving conditions
    if f_name.count("_m") > 0:
        #image width in px
        image_width = 120
        vel = velocity
    else:
        image_width = 60

    pos = (image_height/2. - 0.5, 30. - 0.5)
    dpi = int(image_width/2)

    # loop through the images
    for f in range(film_length):
        canvas = np.zeros((image_height, image_width))

        #move according to linear velocity
        pos = (pos[0], pos[1] + vel)

        #if FEM are included
        if fem == "1":
            pos = (pos[0], pos[1] + rm[f])

        for i in range(image_height):
            for j in range(image_width):
                # the dot
                if f_name.count("dot") > 0:
                    dist = np.sqrt((float(i)-pos[0]) * (float(i)-pos[0]) + (float(j)-pos[1]) * (float(j)-pos[1]))
                    if dist <= radius - 0.5:
                        canvas[i, j] = 1
                    elif radius - 0.5 < dist < radius + 0.5:
                        canvas[i, j] = 4.5 - dist
                # the border
                if f_name.count("border") > 0:
                    x_dist = abs(float(j) - pos[1])
                    if x_dist < border_size - 0.5:
                        canvas[i, j] = 1
                    elif border_size - 0.5 < x_dist < border_size + 0.5:
                        canvas[i, j] = (border_size + 0.5) - x_dist

        # save frame
        fig = plt.figure()
        # fig.set_size_inches(0.25,1)
        fig.set_size_inches(2,  2.*image_height/image_width)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(canvas, cmap='gray')

        plt.savefig(file_location + "/first"+str(f+1).zfill(3)+".png",  dpi=int(dpi))
        plt.close()

        img = cv2.imread(file_location + "/first"+str(f+1).zfill(3)+".png", 0)
        rows, cols = img.shape
        # gaussian blur
        img = cv2.imread(file_location + "/first"+str(f+1).zfill(3)+".png", 0)
        rows, cols = img.shape

        blur = cv2.GaussianBlur(img, (3, 3), 0.5)

        # final image
        fig = plt.figure()
        fig.set_size_inches(2, 2.*image_height/image_width)
        # fig.set_size_inches(0.25,1)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(blur, cmap='gray')

        # plt.savefig(file_location + "/second"+str(f+1).zfill(3)+".png",  dpi = 120)
        plt.savefig(file_location + "/second"+str(f+1).zfill(3)+".png",  dpi=dpi)
        plt.close()
