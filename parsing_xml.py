#!/usr/bin/env python
import xml.etree.ElementTree as ET
#import re   
import argparse
import socket

def valid_ip(ip):
    #return re.match( r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) != None
    #for ip to be valid, it has to be four digit number in range from 0-255
    #dicemal format only: FF.FF.FF.FF in this case considers as invalid
    ips = ip.split('.')
    flag = True
    if len(ips) != 4 :
        flag = False
    else:
        for d in ips :
            if not(d.isdigit() and int(d) > 0 and int(d) < 255):
                flag = False
                break
    return flag

def valid_ip_socketlib(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

if __name__ == '__main__':
    tree = ET.parse("configuration.xml")
    root = tree.getroot()
    dic_iface={}
    for child in root:
        if child.tag == 'server_ip':
            server_ip = child.text
        elif child.tag == 'client_ip':
            client_ip = child.text
        elif child.tag == 'interfaces':
            for sub_child in child:
                #sub_child.get('name') : server_iface name
                #sub_child[0].get('name') : client_iface name
                dic_iface[sub_child.get('name')] = sub_child[0].get('name')

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(description="Parsing xml arguments")
    ap.add_argument("-s", "--server_ip", help="change server ip value")
    ap.add_argument("-c", "--client_ip", help="change client ip value")
    ap.add_argument("-i", "--iface", nargs=2, help="change client ip value")

    args = ap.parse_args()       

    if args.server_ip:
        new_ip = vars(args)["server_ip"]
        if(valid_ip(new_ip)):
            root.find('server_ip').text = new_ip
            tree.write('configuration.xml')
            server_ip = new_ip
        else:
            print "invalid ip"


    if args.client_ip:
        new_ip = vars(args)["client_ip"]
        if(valid_ip(new_ip)):
            root.find('client_ip').text = new_ip
            tree.write('configuration.xml')
            client_ip = new_ip
        else:
            print "invalid ip"

    if args.iface:
        key = vars(args)["iface"][0]
        new_value = vars(args)["iface"][1]
        exist = False
        for siface in root.find('interfaces').findall('server_iface'):
            if siface.get('name') == key:
                siface[0].set('name', new_value)
                exist = True
        if exist:    
            dic_iface[key] = new_value
            tree.write('configuration.xml')
        else:
            print "not exist server interface" 

    print "server_ip: ", server_ip
    print "client_ip: ", client_ip
    print "{:<15} {:<15}".format('server_iface','client_iface')
    for item in dic_iface.items():
        print "{:<15} {:<15}".format(item[0], item[1])

