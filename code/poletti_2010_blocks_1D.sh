#!/bin/bash

#run simulation for input without FEM once
for j in 0
  do

    for i in $j
    do
      # create folders

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/dot ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/dot;
      fi

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/dot_m ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/dot_m;
      fi

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/border ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/border;
      fi

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/border_m ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/border_m;
      fi


      if [ ! -d ../data/poletti2010/blocks/${i}/dot/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/dot/network;
      fi

      if [ ! -d ../data/poletti2010/blocks/${i}/dot_m/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/dot_m/network;
      fi

      if [ ! -d ../data/poletti2010/blocks/${i}/border/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/border/network;
      fi

      if [ ! -d ../data/poletti2010/blocks/${i}/border_m/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/border_m/network;
      fi

      #create images, FEM=0
      python3 01_image_input/image_creation_poletti_2010_1D_blocks.py ${i} 0

      #delete unnecessary files
      cd ../video/img_input/poletti2010/blocks/${i}/dot
      find -type f -name '*first*' -delete
      cd ../dot_m
      find -type f -name '*first*' -delete
      cd ../border
      find -type f -name '*first*' -delete
      cd ../border_m
      find -type f -name '*first*' -delete
      cd ../../../../../../pro

    done

    date
    echo 'STARTING INPUT SIMULATIONS FOR ' ${j}

    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/dot dot_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/border border_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/dot dot_$((j+1)) 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/border border_$((j+1)) 1000

    wait

    date
    echo 'STARTING INPUT SIMULATIONS FOR MOVING ' ${j}

    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/dot_m dot_m_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/border_m border_m_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/dot_m dot_m_$((j+1)) 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/border_m border_m_$((j+1)) 1000

    wait

    for i in $j
    do

      echo "STARTING NETWORK SIMULATIONS FOR " ${i}

      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/dot dot_${i} 32. 16. 1000 dot ${i}
      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/dot_m dot_m_${i} 62. 16. 1000 dot_m ${i}
      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/border border_${i} 32. 16. 1000 border ${i}
      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/border_m border_m_${i} 62. 16. 1000 border_m ${i}

    done
done


#create simulations with FEM
for j in {1..10..2}
  do

    for i in $j $((j+1))
    do
      # create folders

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/dot ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/dot;
      fi

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/dot_m ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/dot_m;
      fi

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/border ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/border;
      fi

      if [ ! -d ../video/img_input/poletti2010/blocks/${i}/border_m ]; then
          mkdir -p ../video/img_input/poletti2010/blocks/${i}/border_m;
      fi


      if [ ! -d ../data/poletti2010/blocks/${i}/dot/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/dot/network;
      fi

      if [ ! -d ../data/poletti2010/blocks/${i}/dot_m/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/dot_m/network;
      fi

      if [ ! -d ../data/poletti2010/blocks/${i}/border/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/border/network;
      fi

      if [ ! -d ../data/poletti2010/blocks/${i}/border_m/network ]; then
          mkdir -p ../data/poletti2010/blocks/${i}/border_m/network;
      fi

      #create images, FEM=1
      python3 01_image_input/image_creation_poletti_2010_1D_blocks.py ${i} 1

      #delete unnecessary files
      cd ../video/img_input/poletti2010/blocks/${i}/dot
      find -type f -name '*first*' -delete
      cd ../dot_m
      find -type f -name '*first*' -delete
      cd ../border
      find -type f -name '*first*' -delete
      cd ../border_m
      find -type f -name '*first*' -delete
      cd ../../../../../../pro
      
    done
    
    date
    echo 'STARTING INPUT SIMULATIONS FOR ' ${j}
    
    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/dot dot_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/border border_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/dot dot_$((j+1)) 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/border border_$((j+1)) 1000

    wait
    
    date
    echo 'STARTING INPUT SIMULATIONS FOR MOVING ' ${j}

    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/dot_m dot_m_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/${j}/border_m border_m_${j} 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/dot_m dot_m_$((j+1)) 1000 &
    python3 02_filter_stages/ms_input.py poletti2010/blocks/$((j+1))/border_m border_m_$((j+1)) 1000

    wait
    
    for i in $j $((j+1))
    do

      echo "STARTING NETWORK SIMULATIONS FOR " ${i}

      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/dot dot_${i} 32. 16. 1000 dot ${i}
      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/dot_m dot_m_${i} 62. 16. 1000 dot_m ${i}
      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/border border_${i} 32. 16. 1000 border ${i}
      python3 03_network/ms_network_no_m.py poletti2010/blocks/${i}/border_m border_m_${i} 62. 16. 1000 border_m ${i}

    done
done
