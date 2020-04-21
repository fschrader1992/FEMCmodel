# FEMCmodel


This directory contains the main programs used for the investigation of the model. Details about the model are given in
 the thesis/paper.

There are two model versions, one with continuous filter stages and a network part used for the motion detection 
mechanism and an entirely continuous one.

From input image creation to final diagrams, for each important step involved in the simulations one example file is put 
in a python notebook to explain the code. Some simulations/conditions required some small changes, so some similar files 
exist. The code should be understandable, after taking a look at the notebooks.

The notebooks are only for explanation. Execute the .sh-files (see below) in order to run a whole simulation from 
beginning to end. In the following there are some remarks first on the files and how they work together and second 
about the simulations of the different experiments.
File Structure
Input Creation

A series of images containing the stimuli is created, used as input for the network. Take a look at the example file for
 the conditions of the Poletti experiment.
Network Implementation

For the network, the processes are split into a file with the different filter stages and one file ontaining the motion 
detector apparatus, implemented as a NEST network.

The continuous filter part takes the created series of images as input and delivers rates as output for all neurons 
(midgets and parasols).
These rates are converted to input for the neurons of the motion detectors. In the simulations only parasol cells 
are evaluated for motion, but another version for midget cells is implemented as well.

Entirely Continuous Version

The entirely continuous version is handled within one file and only for the 1D case. After the continuous filter stages, 
the motion detection mechanism evaluates the signal curve and stores the integrated value in an external file for 
graphics creation.
Evaluation and Figures
Simulations of Poletti et al. (2010)

The simulations of this experiment are conducted with the spiking version of the model. For the evaluation, spike events
 in the center and the outer region are binned in time intervals of length $\Delta t$ and compared. Only, if one of the 
 two areas detected spikes, a motion signal is given. This file replaces the global motion detection network in NEST for
  the experiment. As we are not interested in the properties of this network and less parameters and fine tuning are 
  required, this is a shortcut to get the results produced by the early stages of the model. Two versions, one 
  evaluating the motion detectors, tho other the parasol cells, are implemented.

At the end, histograms of the percentage of bins with differential motion (resembling the experimental results) are 
plotted.
Simulations of Murakami (2003)

For Murakami's On-Line Illusion the entirely continuous model version is used. The integrated amplitude is simply put 
into graphics normalized to the maximum output. There's also a python file to plot the signal strength of midget cells 
for different temporal filter constants (as found in the thesis).
Other Tasks

Images of the Out-Of-Focus as well as movies for Murakami's On-Line Illusion can be created for observation.
Bash scripts

The example files/notebooks are just for explanation. Whole simulations, from input creation to final figure output, 
are managed in bash scripts, ready for execution. Parameters can be changed in the lines

/here will be a list of these scripts.

$\sigma = 2Ddt\alpha$
