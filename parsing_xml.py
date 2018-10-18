#!/usr/bin/env python
import xml.etree.ElementTree as ET
#import re
import argparse
import socket

def valid_ip(ip):
    #return re.match( r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) != None
    #this reguler expression faild, because it didn't handle the case when 
    #ip greater than 256 and still 3 digits. so RE was not the best solution 
   
    #for ip to be valid, it has to be four digit number in range from 0-255
    #dicemal format only: FF.FF.FF.FF in this case considers as invalid
    ips = ip.split('.')
    flag = True
    if len(ips) != 4 :
        print "invalid ip"
        flag = False
    else:
        for d in ips :
            if not(d.isdigit() and int(d) > 0 and int(d) < 255):
                print "invalid ip"
                flag = False
                break
    return flag

#This function works exactly as valid_ip function, but in different way.
def valid_ip_socketlib(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(description="Parsing xml arguments")
    ap.add_argument("-s", "--server_ip", dest="server_ip", help="change server ip value")
    ap.add_argument("-c", "--client_ip", dest="client_ip", help="change client ip value")
    ap.add_argument("-i", "--iface", nargs=2, dest="iface", help="change client ip value")
    ap.add_argument("-b", "--branch", dest="branch", help="change branch value")
    args = ap.parse_args()
    
    tree = ET.parse("configuration.xml")
    root = tree.getroot()
    dic_iface={}
    modify_file = False
    for child in root:
        if child.tag == 'server_ip':
            #If server ip exist and valid, save it and modify the tree, 
            #Else, deal with IP provided from the file
            if args.server_ip and valid_ip(args.server_ip):
                child.text = server_ip = args.server_ip
                modify_file = True
            else:
                server_ip = child.text
        elif child.tag == 'client_ip':
            if args.client_ip and valid_ip(args.client_ip):
                child.text = client_ip = args.client_ip
                modify_file = True
            else:
                client_ip = child.text
        elif child.tag == 'Branch':
            if args.branch:
                child.text = branch = args.branch
                modify_file = True
            else:
                branch = child.text
        elif child.tag == 'interfaces':
            for sub_child in child:
                #sub_child.get('name') : server_iface name
                #sub_child[0].get('name') : client_iface name
                if args.iface and sub_child.get('name') == args.iface[0]:
                    dic_iface[sub_child.get('name')] = args.iface[1]
                    sub_child[0].set('name', args.iface[1])
                    modify_file = True
                else:    
                    dic_iface[sub_child.get('name')] = sub_child[0].get('name')

    if modify_file:
        tree.write('configuration.xml')

    print "server_ip: ", server_ip   #in case of invalid user provided IP, it takes 
                                     #the old IP "from configuration file"
    print "client_ip: ", client_ip
    print "{:<15} {:<15}".format('server_iface','client_iface')
    for item in dic_iface.items():
        print "{:<15} {:<15}".format(item[0], item[1])
    print "Branch: ", branch

