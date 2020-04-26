#!/bin/bash

#VARYING T_P AND T_OFF/T_ON

for k in {1..10}
do 

    if [ ! -d ../video/img_input/murakami2003/${k} ]; then
        mkdir -p ../video/img_input/murakami2003/${k}
    fi
    cd ../video/img_input/poletti2010/blocks/$((k+10))
        cp displacement.data ../../../murakami2003/${k}
    cd ../../../../../pro

    for s in 1 
    do

        for i in 13 27 40
        do
          j=53
          echo simulation $i $j
          if [ ! -d ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i} ]; then
              mkdir -p ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
          fi
          
          if [ ! -d ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network ]; then
              mkdir -p ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network
          fi
          
          python3 01_image_input/image_creation_murakami_2003_1D.py ${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} ${i} ${j} 100 636

          #delete unnecessary files
          cd ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
          find -type f -name '*first*' -delete
          cd ../../../../../pro

        done

        for i in 13 27 40 53 67 80 93
        do
          j=107
          echo simulation $i $j
          if [ ! -d ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i} ]; then
              mkdir -p ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
          fi
          
          if [ ! -d ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network ]; then
              mkdir -p ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network
          fi
          
          python3 01_image_input/image_creation_murakami_2003_1D.py ${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} ${i} ${j} 100 636

          #delete unnecessary files
          cd ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
          find -type f -name '*first*' -delete
          cd ../../../../../pro

        done

        for i in 27 53 80 107 133 160 187
        do
          j=213
          echo simulation $i $j
          if [ ! -d ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i} ]; then
              mkdir -p ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
          fi
          
          if [ ! -d ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network ]; then
              mkdir -p ../data/murakami2003/${k}/zebra_std${s}_on${j}off${i}/network
          fi
          
          python3 01_image_input/image_creation_murakami_2003_1D.py ${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} ${i} ${j} 100 636

          delete unnecessary files
          cd ../video/img_input/murakami2003/${k}/zebra_std${s}_on${j}off${i}
          find -type f -name '*first*' -delete
          cd ../../../../../pro

        done

        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on53off13 zebra_${k}_std${s}_on53off13 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on53off27 zebra_${k}_std${s}_on53off27 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on53off40 zebra_${k}_std${s}_on53off40 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off0 zebra_${k}_std${s}_on107off0 636 

    wait

        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off13 zebra_${k}_std${s}_on107off13 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off27 zebra_${k}_std${s}_on107off27 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off40 zebra_${k}_std${s}_on107off40 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off53 zebra_${k}_std${s}_on107off53 636 

    wait

        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off67 zebra_${k}_std${s}_on107off67 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off80 zebra_${k}_std${s}_on107off80 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on107off93 zebra_${k}_std${s}_on107off93 636

    wait

        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off27 zebra_${k}_std${s}_on213off27 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off53 zebra_${k}_std${s}_on213off53 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off80 zebra_${k}_std${s}_on213off80 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off107 zebra_${k}_std${s}_on213off107 636

    wait

        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off133 zebra_${k}_std${s}_on213off133 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off160 zebra_${k}_std${s}_on213off160 636 &
        python3 02_filter_stages/ms_input.py murakami2003/${k}/zebra_std${s}_on213off187 zebra_${k}_std${s}_on213off187 636 

    wait

        for i in 13 27 40
        do
          j=53
          echo simulation $i $j
          
          python3 03_network/ms_network_no_m.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}
          
        done
        
        for i in 0 13 27 40 53 67 80 93
        do
          j=107
          echo simulation $i $j
          
          python3 03_network/ms_network_no_m.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}
          
        done
        
        for i in 27 53 80 107 133 160 187
        do
          j=213
          echo simulation $i $j
          
          python3 03_network/ms_network_no_m.py murakami2003/${k}/zebra_std${s}_on${j}off${i} zebra_${k}_std${s}_on${j}off${i} 62. 16. 636 ${j} ${i}
          
        done

    done
done
