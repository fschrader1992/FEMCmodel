#!/bin/bash

#VARYING SIGMA FORM MIDGETS, NETWORK PART ONLY

for k in {1..6..2}
do 

    #values of sigma (percent of normal value)
    for s in {0..150..50}
    do
            for i in 0 #80
            do
              j=107
              echo simulation $i $j

              python3 03_network/ms_network_no_p.py jitter_fem/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}
              python3 03_network/ms_network_no_p.py jitter_fem/$((k+1))/zebra_std${s}_on${j}off${i} zebra_$((k+1))_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}

              python3 03_network/ms_network_no_p.py jitter_fem/${k}/zebra_std$((s+25))_on${j}off${i} zebra_${k}_std$((s+25))_on${j}off${i} 62. 16. 636 ${j} ${i}
              python3 03_network/ms_network_no_p.py jitter_fem/$((k+1))/zebra_std$((s+25))_on${j}off${i} zebra_$((k+1))_std$((s+25))_on${j}off${i} 62. 16. 636 ${j} ${i}

            done

    done
done
