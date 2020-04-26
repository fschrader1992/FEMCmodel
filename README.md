# FEMCmodel

This directory contains the main programs used for the investigation of the fixational eye movement compensating (FEMC) 
model. Details about the model are given in the paper.

Execute the .sh-files (see below) in order to run a whole simulation from beginning to end. In the following
some short remarks on the files and how they work together.

## File Structure

The files are located in the code directory. For each simulation there are four steps:

1. Image creation for input
2. Simulation of the filter stages, creating a continuous signal for midget and parasol cells
3. Simulation of the network part (separated for parasol and midget cells), converting the signal to spikes
4. Motion detection stages and evaluation, including plots

For the experiments by Poletti et al. (2010), steps 1-3 are handled by the script
[poletti_2010_blocks_1D.sh](code/poletti_2010_blocks_1D.sh). For Murakami's On-Line illusion (2003), be sure to run both
scripts, the one for varying the standard deviation $\sigma$ [murakami_2003_sigma.sh](code/murakami_2003_sigma.sh) and 
the one with varying ($t_p$, $t_off$) for the illusion [murakami_2003_illusion.sh](code/murakami_2003_illusion.sh)
itself. The fourth step is handled by two jupyter notebooks. Here you can adapt the parameters for the motion detection
stage and plots.
All files are commented for clarity.

The network part only simulates parasol cells to speed up code. If you are interested in midget cells' behaviour, you
can run the network part and evaluation for midgets with the scripts labelled as "network_midgets" and the notebooks.

A calibration file allows to set spiking rates.
