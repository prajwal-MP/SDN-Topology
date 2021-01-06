# SDN-Topology


Download mininet VM image from http://mininet.org/download/
edit router_config to configure routers
edit PCA and PCB1 for creating topology

HOW TO USE
[1] open multiple mininet VM's and note down their IP's

[1*] It is recommended that you ssh into these rather than run the commands on them directly 
      ex:- ssh mininet@192.168.x.x

[2] sudo python PCA.py in first VM
    sudo python PCB1.py in second VM

[3] The following commands should be run once mininet starts in each VM

zebra -g root  -f /usr/local/etc/r1zebra.conf -d -z ~/r1zebra.api -i ~/r1zebra.interface
ospfd -g root  -f /usr/local/etc/r1ospfd.conf -d -z ~/r1zebra.api -i ~/r1ospfd.interface

[4] now ping from one vm to other. The routers are SDN and will learn paths quickly reducing the time taken after one or two pings.

[0] You can also run RL.py for Reinforcement algorithm as router. This needs to be trained sufficiently to actually give good results
