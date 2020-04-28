import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cv2
import sys

plt.switch_backend('agg')


#PARAMETERS-------------------------------------------------------------------------------------------------------------

# from input
#file directory
file_loc = sys.argv[1]
#suffix for simulation
suff = sys.argv[2]
#t_p
cyc1 = float(sys.argv[3])
#t_on
cyc2 = float(sys.argv[4])
#ampiltude of sigma as percentage of normal value
ampl = float(sys.argv[5])
#simulation length
film_length = int(sys.argv[6])

set_fem_path = 0
if len(sys.argv) == 8:
    print("CREATED")
    set_fem_path = int(sys.argv[7])

print("IMAGE CREATION BLOCKS " + suff)

file_location = "../video/img_input/murakami2003/" + str(file_loc) + "/"

image_height = 30
image_width = 120
#size of simulated bar in arcmin -> px = 2 times
border_size = 30.
#if you want to set velocity to 30 arcmin/s (e.g. for testing) -> 60px/1000ms
#velocity = 0.06
#else additional velocity is zero
vel = 0

#image dpi
dpi = int(image_width/2)


#FEM--------------------------------------------------------------------------------------------------------------------

# for normal distributed FEM
sigma = 0.632

# get normal 2d distribution
# use this to get same statistics as for actual 2D random walk -> use only x-component

#create data once
if set_fem_path == 1:
    mean = [0, 0]
    cov = [[1, 0], [0, 1]]
    tl_x, tl_y = sigma*np.random.multivariate_normal(mean, cov, film_length).T

    d_data = open(file_location + '../displacement.data', 'wb')
    np.save(d_data, (tl_x, tl_y))
    d_data.close()

d_data = open(file_location + '../displacement.data', 'rb')
(rm, t_y) = np.load(d_data)

#for varying sigma
rm = 0.01 * ampl * rm


#BLANK-IMAGE------------------------------------------------------------------------------------------------------------

#first save the blank image without stimulus (t_off)
canvas2 = 0.5*np.ones((image_height, image_width))

fig = plt.figure()
fig.set_size_inches(image_width/image_height, 1)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(canvas2, cmap='gray', norm=colors.Normalize(vmin=0., vmax=1.))
plt.savefig(file_location + "first_blank.png",  dpi = int(image_height))
plt.close()


#CREAT_MOVING-IMAGES----------------------------------------------------------------------------------------------------

#set initial position
pos = (image_height/2. - 0.5, image_width/2)

# loop through images
for f in range(film_length):
    canvas = np.zeros((image_height, image_width))

    #move according to FEM
    pos = (pos[0], pos[1] + rm[f])

    for i in range(image_height):
        for j in range(image_width):
            #bar
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


    #put images together
    img1 = cv2.imread(file_location + "first"+str(f+1).zfill(3)+".png",0)
    img2 = cv2.imread(file_location + "first_blank.png",0)

    if cyc1 > 0.:
        if f % int(cyc2) >= int(cyc2 - cyc1):
            img = img2
        else:
            img = img1
    else:
        img = img1

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
