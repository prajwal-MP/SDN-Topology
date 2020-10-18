#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Link, Intf
import time
import os

class LinuxRouter( Node ):
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        super( LinuxRouter, self ).terminate()


def run():
    NODE1_IP='192.168.159.130'
    NODE2_IP='192.168.159.129'
    net = Mininet(controller = None, topo=None )
    net.addController('c0',
                      controller=RemoteController,
                      ip='192.168.159.129',
                      port=6633, topo=None)
    r2 = net.addHost( 'r2', cls=LinuxRouter, ip='30.0.0.2/24' )
    h2 = net.addHost( 'h2', ip='30.0.0.10/24')
    s2 = net.addSwitch('s2')
    net.addLink(s2,r2,intfName2='s2-eth1',params2={ 'ip' : '30.0.0.2/24' })
    net.addLink(s2,h2,intfName2='s2-eth2',params2={ 'ip' : '30.0.0.10/24' })

    r2.cmd('sudo zebra -g root  -f /usr/local/etc/r1zebra.conf -d -z ~/r1zebra.api -i ~/r1zebra.interface')
    r2.cmd('sudo ospfd -g root  -f /usr/local/etc/r1ospfd.conf -d -z ~/r1zebra.api -i ~/r1ospfd.interface')
    s2.cmd('ip li ad s2-gre1 type gretap local '+NODE2_IP+' remote '+NODE1_IP+' ttl 64')
    s2.cmd('ip li se dev s2-gre1 up')
    
#    Intf('tunnel_2_1',node=s2)
#    Intf('tunnel_2_2',node=s2)
    Intf('s2-gre1',node=s2)
    s2.cmdPrint('route')
    net.start()
    
    CLI( net )
    net.stop()
    os.system("killall -9 ospfd")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

