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
    r1 = net.addHost( 'r1', cls=LinuxRouter, ip='20.0.0.1/24' )
    h1 = net.addHost( 'h1', ip='20.0.0.10/24')
    net.addLink(h1,r1,intfName2='r1-eth1',params2={ 'ip' : '20.0.0.1/24' })
    r1.cmd('sudo zebra -g root  -f /usr/local/etc/r1zebra.conf -d -z ~/r1zebra.api -i ~/r1zebra.interface')
    r1.cmd('sudo ospfd -g root  -f /usr/local/etc/r1ospfd.conf -d -z ~/r1zebra.api -i ~/r1ospfd.interface')
    #Intf('tunnel_1_1',node=r1)
    #Intf('tunnel_1_2',node=r1)
    r1.cmd('ip li ad r1-gre1 type gretap local '+NODE1_IP+' remote '+NODE2_IP+' ttl 64')
    r1.cmd('ip li se dev r1-gre1 up')
    Intf('r1-gre1',node=r1)
    r1.cmdPrint('route')
    net.start()
    CLI( net )
    net.stop()
    os.system("killall -9 ospfd")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()

