#!/bin/bash

#create simulations with FEM -> take simulation number 0
for j in 0
  do

    for i in ${j}
    do

      echo "STARTING NETWORK SIMULATIONS FOR " ${i}

      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/dot dot_${i} 32. 16. 1000 dot ${i}
      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/dot_m dot_m_${i} 62. 16. 1000 dot_m ${i}
      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/border border_${i} 32. 16. 1000 border ${i}
      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/border_m border_m_${i} 62. 16. 1000 border_m ${i}

    done
done



#create simulations with FEM
for j in {1..10..2}
  do

    for i in ${j} $((j+1))
    do

      echo "STARTING NETWORK SIMULATIONS FOR " ${i}

      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/dot dot_${i} 32. 16. 1000 dot ${i}
      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/dot_m dot_m_${i} 62. 16. 1000 dot_m ${i}
      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/border border_${i} 32. 16. 1000 border ${i}
      python3 03_network/ms_network_only_p.py poletti2010/blocks/${i}/border_m border_m_${i} 62. 16. 1000 border_m ${i}

    done
done
