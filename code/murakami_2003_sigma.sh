#!/bin/bash

#VARYING SIGMA

for k in {1..6..2}
do 

    if [ ! -d ../video/img_input/murakami2003/${k} ]; then
        mkdir -p ../video/img_input/murakami2003/${k}
    fi
    
    if [ ! -d ../video/img_input/murakami2003/$((k+1)) ]; then
        mkdir -p ../video/img_input/murakami2003/$((k+1))
    fi

    #values of sigma (percent of normal value)
    for s in {0..150..50}
    do

            for i in 0
            do
              j=107
              echo simulation $i $s
              if [ ! -d ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i} ]; then
                  mkdir -p ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
              fi

              if [ ! -d ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network ]; then
                  mkdir -p ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network
              fi

              echo simulation $i $((s+25))
              if [ ! -d ../video/img_input/murakami2003/${k}/zebra_std$((s+25))_on${j}off${i} ]; then
                  mkdir -p ../video/img_input/murakami2003/${k}/zebra_std$((s+25))_on${j}off${i}
              fi

              if [ ! -d ../data/murakami2003/${k}/zebra_std$((s+25))_on${j}off${i}/network ]; then
                  mkdir -p ../data/murakami2003/${k}/zebra_std$((s+25))_on${j}off${i}/network
              fi

              python3 01_image_input/image_creation_murakami_2003_1D.py ${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} ${i} ${j} ${s} 636
              python3 01_image_input/image_creation_murakami_2003_1D.py ${k}/zebra_std$((s+25))_on${j}off${i} zebra_${k}_std$((s+25))_on${j}off${i} ${i} ${j} $((s+25)) 636

              #delete unnecessary files
              cd ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
                  find -type f -name '*first*' -delete
              cd ../../../../../code
              cd ../video/img_input/murakami2003/${k}/zebra_std$((s+25))_on${j}off${i}
                  find -type f -name '*first*' -delete
              cd ../../../../../code
              
              
              
              if [ ! -d ../video/img_input/murakami2003/$((k+1))/zebra_std${s}_on${j}off${i} ]; then
                  mkdir -p ../video/img_input/murakami2003/$((k+1))/zebra_std${s}_on${j}off${i}
              fi

              if [ ! -d ../data/murakami2003/$((k+1))/zebra_std${s}_on${j}off${i}/network ]; then
                  mkdir -p ../data/murakami2003/$((k+1))/zebra_std${s}_on${j}off${i}/network
              fi

              echo simulation $i $((s+25))
              if [ ! -d ../video/img_input/murakami2003/$((k+1))/zebra_std$((s+25))_on${j}off${i} ]; then
                  mkdir -p ../video/img_input/murakami2003/$((k+1))/zebra_std$((s+25))_on${j}off${i}
              fi

              if [ ! -d ../data/murakami2003/$((k+1))/zebra_std$((s+25))_on${j}off${i}/network ]; then
                  mkdir -p ../data/murakami2003/$((k+1))/zebra_std$((s+25))_on${j}off${i}/network
              fi


              python3 01_image_input/image_creation_murakami_2003_1D.py $((k+1))/zebra_std${s}_on${j}off${i} zebra_$((k+1))_std${s}_on${j}off${i} ${i} ${j} ${s} 636
              python3 01_image_input/image_creation_murakami_2003_1D.py $((k+1))/zebra_std$((s+25))_on${j}off${i} zebra_$((k+1))_std$((s+25))_on${j}off${i} ${i} ${j} $((s+25)) 636

              #delete unnecessary files
              cd ../video/img_input/murakami2003/$((k+1))/zebra_std${s}_on${j}off${i}
                  find -type f -name '*first*' -delete
              cd ../../../../../code
              cd ../video/img_input/murakami2003/$((k+1))/zebra_std$((s+25))_on${j}off${i}
                  find -type f -name '*first*' -delete
              cd ../../../../../code

            done

            python3 02_filter_stages/ms_input.py murakami2003/$((k))/zebra_std${s}_on107off0 zebra_$((k))_std${s}_on107off0 636 &
            python3 02_filter_stages/ms_input.py murakami2003/$((k))/zebra_std$((s+25))_on107off0 zebra_$((k))_std$((s+25))_on107off0 636 &
            python3 02_filter_stages/ms_input.py murakami2003/$((k+1))/zebra_std${s}_on107off0 zebra_$((k+1))_std${s}_on107off0 636 &
            python3 02_filter_stages/ms_input.py murakami2003/$((k+1))/zebra_std$((s+25))_on107off0 zebra_$((k+1))_std$((s+25))_on107off0 636

            wait

            for i in 0
            do
              j=107
              echo simulation $i $j

              python3 03_network/ms_network_only_p.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}
              python3 03_network/ms_network_only_p.py murakami2003/$((k+1))/zebra_std${s}_on${j}off${i} zebra_$((k+1))_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}

              python3 03_network/ms_network_only_p.py murakami2003/${k}/zebra_std$((s+25))_on${j}off${i} zebra_${k}_std$((s+25))_on${j}off${i} 62. 16. 636 ${j} ${i}
              python3 03_network/ms_network_only_p.py murakami2003/$((k+1))/zebra_std$((s+25))_on${j}off${i} zebra_$((k+1))_std$((s+25))_on${j}off${i} 62. 16. 636 ${j} ${i}

            done

    done
done
