'''
THIS IS THE PART OF THE NEURAL NETWORK.
IT TAKES THE VALUES TO CALCULATE THE MEMBRANE POTENTIALS OF THE INPUT NEURONS AND THEN CALCULATES THE NETWORK OUTPUT
the unit in space is 1arcmin!
'''

import numpy as np
import sys
import matplotlib.pyplot as plt
import nest
import nest.raster_plot
import nest.topology as tp

pgf_with_rc_fonts = {"font.family": "serif", "font.serif": [], "font.sans-serif": []}
plt.rcParams.update(pgf_with_rc_fonts)

nest.ResetKernel()

msd = 1000
nest.SetKernelStatus({'local_num_threads' : 4})
n_vp = nest.GetKernelStatus('total_num_virtual_procs')
msdrange1 = range(msd, msd+n_vp)
pyrngs = [np.random.RandomState(s) for s in msdrange1]
msdrange2 = range(msd+n_vp+1, msd+1+2*n_vp)
nest.SetKernelStatus({'grng_seed': msd+n_vp,
                      'rng_seeds': msdrange2})

I_E = 355.

def set_I_e_random(layer):
    r = nest.GetNodes(layer)[0]
    node_info = nest.GetStatus(r)
    localnodes = [(ni['global_id'], ni['vp']) for ni in node_info if ni['local']]
    for gid, vp in localnodes:
        nest.SetStatus([gid], {'I_e' : I_E + pyrngs[vp].uniform(-2., 2.)})


#INPUT-RATES-FROM-MS_INPUT----------------------------------------------------------------------------------------------

extent = 121.

t_start = 0

weight = 40.
weight_std = 0.5
mdw = 4.0

sim_title = sys.argv[1]
handle_name = sys.argv[2]
#extend equals half the size of the input image in px
extent_x = float(sys.argv[3])
extent_y = float(sys.argv[4])
sim_length = int(float(sys.argv[5]))
#for Murakami(2003), t_on and t_off
exp_nr = sys.argv[6]
cond_nr = sys.argv[7]
sim_title_2 = ''


t_end = sim_length

center_x = extent_x/2.
center_y = extent_y/2.

#get membrane potentials
m_file = open('../data/'+str(sim_title)+'/midget_rates_'+str(handle_name)+'_on.data', 'rb')
m_data = np.load(m_file)
m_file.close()

midget_rates = m_data

#amplification of membrane potential, calibrated to moving bar stimulus
mmr = 8.

midget_rates = mmr*midget_rates #+m_noise

#for rates
mrs = []


#NETWORK-PART-----------------------------------------------------------------------------------------------------------
#INITIALIZE-NEURONS-----------------------------------------------------------------------------------------------------

#definitions
nest.CopyModel("iaf_psc_alpha", "iaf_psc_alpha_mp")
nest.CopyModel("iaf_psc_alpha", "iaf_psc_alpha_i", {"I_e" : I_E})
nest.CopyModel("spike_detector", "my_spike_detector", {"withgid": True,
                                                       "withtime": True,
                                                       "to_memory": True})

nest.CopyModel('static_synapse', 'ex', {'weight': 1.0})


#CREATE-LAYERS----------------------------------------------------------------------------------------------------------

#get positions
gm_file = open('../data/' + str(sim_title) + str(sim_title_2) + '/m_pos_' + handle_name + '.data', 'rb')
gm_data = np.load(gm_file)
gm_file.close()
gm_data = gm_data.tolist()

gm_pos = []

for i in range(len(gm_data)):
    for j in range(len(gm_data[0])):
        mrs += [midget_rates[:, i, j]]
        gm_pos += [[0.5*gm_data[i][j][0]+0.25, 0.5*gm_data[i][j][1]+0.25]]

#create layer for input
midgets = tp.CreateLayer({'extent' : [extent_x, extent_y], 'center' : [center_x, center_y], 'positions' : gm_pos,
                            'elements': 'iaf_psc_alpha_mp', 'edge_wrap': True})

#detect spikes
out_m = tp.CreateLayer({'extent' : [extent_x, extent_y], 'center' : [center_x, center_y], 'positions' : gm_pos,
                        'elements': 'my_spike_detector'})


#CREATE-CONNECTIONS-----------------------------------------------------------------------------------------------------

out_conndict = {'connection_type' : 'convergent', 'mask' : {'rectangular' : {'lower_left' : [-0.2, -0.2],
                                                                             'upper_right' : [0.2, 0.2]}}}

tp.ConnectLayers(midgets, out_m, out_conndict)


#SIMULATION-------------------------------------------------------------------------------------------------------------

#for updates
PIDs = nest.GetNodes(midgets)

for f in range(t_start, t_end):
    print(handle_name + ' '+ str(f))
    #reset potential
    for n in range(len(PIDs[0])):
        qr = mrs[n][f]
        nest.SetStatus([PIDs[0][n]], {'I_e': qr})
    #run simulation
    nest.Simulate(1)


#SAVE-OUTPUT------------------------------------------------------------------------------------------------------------

def save_spikes(layer_name, layer):
    '''
    :param layer_name: name of layer to be printed
    :param layer: output layer containing spike event times
    :return:
    '''
    directory = '../data/' + str(sim_title) + '/network/'

    sm_file = open(directory+'/'+layer_name+'_'+handle_name+'.txt', 'w+')
    for n in range(len(layer[0])):
        #get spike events
        n_evs = nest.GetStatus([layer[0][n]], "n_events")[0]
        if n_evs > 0:
            sm_file.write(str(layer[0][n]) + '\t' + str(nest.GetStatus([layer[0][n]], "events")[0]["times"]) + '\n')
    sm_file.close()
    return 0


#save layer neuron IDs, to assign spikes to neurons in next step
GID_file = open('../data/'+str(sim_title)+'/network/GID_m_info.txt', 'w+')
#get IDs from output layer
layerIDs = nest.GetNodes(out_m)
GID_file.write('midgets \t'+str(layerIDs[0][0])+'\t'+str(layerIDs[0][len(layerIDs[0])-1])+'\n')

#save spike times and position (neuron ID)
save_spikes('spikes_midgets', layerIDs)

GID_file.close()

#set to zero
parasols = 0
out_m = 0

print(str(handle_name) + 'finished')

sys.exit()
