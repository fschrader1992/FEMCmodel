#!/bin/bash

#VARYING T_P AND T_OFF/T_ON

#It is important that the simulaiton for t_off=0 and t_p=107 runs first, as the image creation creates and saves
#FEM data only then and will be called otherwise.

for k in {1..10}
do 

    for s in 1 
    do

        for i in 13 27 40
        do
          j=53
          echo simulation $i $j

          python3 03_network/ms_network_only_p.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}

        done

        for i in 0 13 27 40 53 67 80 93
        do
          j=107
          echo simulation $i $j

          python3 03_network/ms_network_only_p.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}

        done

        for i in 27 53 80 107 133 160 187
        do
          j=213
          echo simulation $i $j

          python3 03_network/ms_network_only_p.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}

        done

    done
done
