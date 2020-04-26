'''
THIS PART READS THE PIXELS OF A MOVIE AND APPLIES THE FILTERS TO THE PROPOSED MODEL FOR MICROSACCADES.
THE OUTPUT ARE MIDGET AND PARASOL CELL POTENTIAL VALUES.
'''

import sys
import os
import glob
import cv2
import datetime
import itertools
import copy
import numpy as np
import matplotlib.pyplot as plt


#DEFINE-FILTER-FUNCTION-------------------------------------------------------------------------------------------------

def temp_filter_fct(t, tau1, tau2, p):
    return 25./20.*(t*t*t/(tau1*tau1*tau1*tau1)*np.exp(-t/tau1)-p*t*t*t/(tau2*tau2*tau2*tau2)*np.exp(-t/tau2))

def spatial_filter_fct(x, x0, sigma, alpha, beta):
    return (np.exp(-(x-x0)*(x-x0)/(2*sigma*sigma))-alpha*np.exp(-(x-x0)*(x-x0)/(2*beta*beta*sigma*sigma)))/sigma


#LOAD-FRAMES------------------------------------------------------------------------------------------------------------

now = datetime.datetime.now()

pgf_with_rc_fonts = {"font.family": "serif", "font.serif": [], "font.sans-serif": []}
plt.rcParams.update(pgf_with_rc_fonts)

#variable paramaters given in command line
#simulation name
sim_title = sys.argv[1]
#handle (short version of name)
handle_name = sys.argv[2]
#frame number = simulated time in ms
fn = sys.argv[3]


#read image files from dir (processed image labelled as second001 etc.)
frames = []
frame_number = int(fn)

os.chdir("../video/img_input/" + sim_title)
for file in glob.glob("second*.png"):
    frames += [file]
frames.sort()

#get image dimensions in px, 1px = 0.5arcmin
f = cv2.imread(frames[0])
height, width = f.shape[:2]
print(height, width)

#this is the list that contains the pixel values (gray) in (t, y, x)
pixel4d = np.zeros(shape=(frame_number, height, width))

#fill list
for f, file in enumerate(frames):
    frame = cv2.imread(file)
    #store 2D array in pixel4d
    pixel4d[f] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(float)

cv2.destroyAllWindows()
#change directory
curr_dir = sim_title.count("/")
up_dirs_str = ""
for cd_ct in range(curr_dir):
    up_dirs_str += "../"
os.chdir(up_dirs_str + "../../../code/02_filter_stages")


#INITIALIZE-------------------------------------------------------------------------------------------------------------

#set all parameters

#time step in ms
dt = 1.

#temporal filter constants for function
#A*(t**3/(tau1**4)*exp(-t/tau1)-p*t**3/(tau2**4)*exp(-t/tau2))
#A is set to 5/4 in ms_functions.

#temporal constant 1
tau1 = 10.
#temporal constant 2
tau2 = 15.
#weight negative/positive contribution
p = .65

temp_filter_cut_off = 200

#spatial filter constants for DoG function
#1/sigma*exp(-(x-x0)**2/(2*sigma**2))-alpha*1/sigma*exp(-(x-x0)**2/(2*beta**2*sigma**2))
#note: it is not possible to simply calculate the values for each pixel within a spatial filter once,
#as each midget cell is shifted relatively to the background due to the hexagonal structure.

#weight negative/positive contribution
alpha = .1
#surround/center ration
beta = 3.
#center field sigma in pixel
sigma = 1.

#cut-off radius in pixel for spatial filter
mid_sf_br = 6
par_sf_br = 2*mid_sf_br

#other values related to space
#pixel to receptor/midgets ratio, needed for receptor distance/number
px_mid_ratio = 1.
#distance of midgets
midget_dist = px_mid_ratio
#in arcmin
px_dist = 0.5
#ratio determines
#	- number of midget/parasol cells
# 	- respective RF width (mid_par_ratio*sigma)
#	- distance between parasol cells
mid_par_ratio = 4.

#get grid dimensions
#the grid is hexagonal, thus from row to row the height difference is weighted by cos(30deg) = 0.866
midget_height = int(height/(px_mid_ratio*0.866))
midget_width = int(width/px_mid_ratio)

parasol_height = int(height/(px_mid_ratio*mid_par_ratio*0.866))
parasol_width = int(width/(px_mid_ratio*mid_par_ratio))

print(midget_height, midget_width, parasol_height, parasol_width)

#array to store all midget/parasol values at (x, y, t)
midgets4d = np.zeros(shape=(frame_number, midget_height, midget_width))
parasols4d = np.zeros(shape=(frame_number, parasol_height, parasol_width))

#for cell positions
midget_grid = np.zeros(shape=(midget_height, midget_width, 2))
parasol_grid = np.zeros(shape=(parasol_height, parasol_width, 2))


#MIDGETS-SPATIAL-FILTERS------------------------------------------------------------------------------------------------

print('---')
print('start of midget spatial part ' + handle_name)

#apply periodic boundary conditions -> copy and append pixel values
pixel4d = np.append(pixel4d, pixel4d[:, :, :(mid_sf_br)], axis=2)
pixel4d = np.append(pixel4d[:, :, (len(pixel4d[0, 0]) - mid_sf_br):], pixel4d, axis=2)

pixel4d = np.append(pixel4d, pixel4d[:, :mid_sf_br, :], axis=1)
pixel4d = np.append(pixel4d[:, (len(pixel4d[0]) - mid_sf_br):, :], pixel4d, axis=1)


def get_spat_filter_midget(ij):
    '''
    :param ij: array position of midget cell
    :return: spatially filtered input value of midget cell at time t
    '''

    #print info
    if ij[0] % 5 == 0:
        if ij[1] == 0:
            print(handle_name + ' ' + str(ij[0]))

    #get position
    #cos(30deg)
    pos_i = 0.866*ij[0]
    pos_j = ij[1]

    if ij[0]%2 == 0:
        pos_j += 0.5

    #set cell coordinates in grid
    midget_grid[ij[0]][ij[1]][0] = pos_j
    midget_grid[ij[0]][ij[1]][1] = pos_i

    #next is the part for calculation of the spatial filter weights
    #due to the hexagonal grid, the distances are different for each midget cell, thus needs to be dne in every step

    #get the range of pixel within RF
    #all i with dist < r_break
    i_low = int(pos_i*px_mid_ratio-mid_sf_br)
    i_ceil = int(pos_i*px_mid_ratio+mid_sf_br)+1
    # all j with dist < _break
    j_low = int(pos_j*px_mid_ratio-mid_sf_br)
    j_ceil = int(pos_j*px_mid_ratio+mid_sf_br)+1

    #get weights
    (tt, yy, xx) = np.mgrid[0:frame_number, i_low:i_ceil, j_low:j_ceil]

    z = spatial_filter_fct(np.sqrt(0.866*(pos_i-yy)*0.866*(pos_i-yy)+(pos_j-xx)*(pos_j-xx)), 0, sigma, alpha, beta)

    #shift, because of periodic bc earlier appended array at beginning
    i_low += mid_sf_br
    i_ceil += mid_sf_br
    j_low += mid_sf_br
    j_ceil += mid_sf_br

    #apply filter and get midget potential for all frames
    qrt = np.sum(z*pixel4d[:, i_low:i_ceil, j_low:j_ceil], axis=1)
    midgets4d[:, ij[0], ij[1]] = np.sum(qrt, axis=1)


#apply the spatial filter (call function from above)
#iterate through list of midgets
list(map(lambda x: get_spat_filter_midget(x), itertools.product(range(midget_height), range(midget_width))))


#MIDGETS-TEMPORAL-FILTERS-----------------------------------------------------------------------------------------------

print('---')
print('start of midget temporal part ' + handle_name)

#calculate the values for the temporal filter
(tt, yy, xx) = np.mgrid[0:temp_filter_cut_off, :midget_height, :midget_width]

temp_filter = temp_filter_fct(tt*dt, tau1, tau2, p)
#the filter is reversed in time
temp_filter = temp_filter[::-1, :, :]
#fill with zeros, such that np.roll() is possible
temp_filter = np.append(temp_filter, np.zeros((frame_number, midget_height, midget_width)), axis=0)

#output array
midgets4d_temp = np.zeros(shape=(frame_number, midget_height, midget_width))

#apply temporal filter
for f in range(frame_number):
    if f % 100 == 0:
        print(handle_name + ' time step ' + str(f))
    midgets4d_temp[f] = np.sum(temp_filter[temp_filter_cut_off:]*midgets4d, axis=0)
    temp_filter = np.roll(temp_filter, 1, axis=0)

#rectification
midgets4d_temp_on = np.where(midgets4d_temp < 0, 0, midgets4d_temp)


#PARASOLS-SPATIAL-FILTERS-----------------------------------------------------------------------------------------------

print('---')
print('start of parasol part ' + handle_name)

#different distances in y-direction
par_sf_br_v = int(1./0.866*par_sf_br)

#set parasol cell spatial filter
#as in grid with midgets, just needs to be done once
#set boundaries for midgets in spatial filter
i_low = -par_sf_br_v
i_ceil = par_sf_br_v + 1
j_low = -par_sf_br
j_ceil = par_sf_br + 1

#calculate filter
(tt, yy, xx) = np.mgrid[0:frame_number, i_low:i_ceil, j_low:j_ceil]
par_sf = spatial_filter_fct(np.sqrt(0.866*yy*0.866*yy + xx*xx), 0, mid_par_ratio*sigma, alpha, beta)

#apply periodic boundary conditions to input
#copy to save original later
m4d = copy.deepcopy(midgets4d_temp_on)

m4d = np.append(m4d, m4d[:, :, :(par_sf_br + 1)], axis=2)
m4d = np.append(m4d[:, :, (len(m4d[0, 0]) - par_sf_br):], m4d, axis=2)

m4d = np.append(m4d, m4d[:, :(par_sf_br_v + 1), :], axis=1)
m4d = np.append(m4d[:, (len(m4d[0]) - par_sf_br_v):, :], m4d, axis=1)


def get_spat_filter_parasol(ij):
    '''
    :param ij: array position of midget cell
    :return: spatially filtered input value of midget cell at time t
    '''

    #print info
    if ij[0]%5 == 0:
        if ij[1] == 0:
            print(handle_name + ' ' + str(ij[0]))

    #get position
    pos_i = 0.866*mid_par_ratio*ij[0]
    pos_j = mid_par_ratio*ij[1]

    if ij[0]%2 == 0:
        pos_j += mid_par_ratio*0.5

    parasol_grid[ij[0]][ij[1]][0] = pos_j
    parasol_grid[ij[0]][ij[1]][1] = pos_i

    #get the range of pixels within RF
    #shift, because of periodic bc earlier appended array at beginning
    i_low = int(mid_par_ratio)*ij[0]
    i_ceil = int(mid_par_ratio)*ij[0] + 2*par_sf_br_v + 1
    j_low = int(mid_par_ratio)*ij[1]
    j_ceil = int(mid_par_ratio)*ij[1] + 2*par_sf_br + 1

    #get filtered values
    qrt = np.sum(par_sf * m4d[:, i_low:i_ceil, j_low:j_ceil], axis=1)
    parasols4d[:, ij[0], ij[1]] = np.sum(qrt, axis=1)

#apply the spatial filter
list(map(lambda x: get_spat_filter_parasol(x), itertools.product(range(parasol_height), range(parasol_width))))

#rectification
parasols4d_on = np.where(parasols4d < 0, 0, parasols4d)


#SAVE-OUTPUT------------------------------------------------------------------------------------------------------------

print('save ' + handle_name)

#save cell positions
m_pos_data = open('../../data/'+sim_title+'/m_pos_'+str(handle_name)+'.data', 'wb')
np.save(m_pos_data, midget_grid)
m_pos_data.close()

p_pos_data = open('../../data/'+sim_title+'/p_pos_'+str(handle_name)+'.data', 'wb')
np.save(p_pos_data, parasol_grid)
p_pos_data.close()

#save cell membrane potential
m_data = open('../../data/'+sim_title+'/midget_rates_'+str(handle_name)+'.data', 'wb')
np.save(m_data, midgets4d_temp)
m_data.close()

p_data = open('../../data/'+sim_title+'/parasol_rates_'+str(handle_name)+'.data', 'wb')
np.save(p_data, parasols4d)
p_data.close()

m_data = open('../../data/'+sim_title+'/midget_rates_'+str(handle_name)+'_on.data', 'wb')
np.save(m_data, midgets4d_temp_on)
m_data.close()

p_data = open('../../data/'+sim_title+'/parasol_rates_'+str(handle_name)+'_on.data', 'wb')
np.save(p_data, parasols4d_on)
p_data.close()

print('--- PROGRAM FINISHED ---')
sys.exit()
