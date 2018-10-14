#!/usr/bin/env python
#import required packages 
import re 		#for reguler expressions 
import argparse		
import socket 

def update_file(old_value, new_value):
    global config
    xml_file = open('configuration.xml', 'w') 
    config=config.replace(old_value, new_value)
    xml_file.write(config)
    xml_file.close() 

def valid_ip(ip):
    #return re.match( r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) != None 
    #for ip to be valid, it has to be for digit number in range from 0-255
    #Valid if its in dicemal format only
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

#main
xml_file = open('configuration.xml', 'r') 
config =  xml_file.read()
xml_file.close()

server_ip = re.search( r'<server_ip>.*</server_ip>', config).group()

#IP: four numbers seperated by dot DD.DD.DD.DD
ipre = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    
if(server_ip != None):
   server_ip = re.search( ipre, server_ip).group() 

client_ip = re.search( r'<client_ip>.*</client_ip>', config).group()
if(client_ip != None):
    client_ip = re.search( ipre, client_ip).group()

server_iface=re.findall( r'<server_iface.*', config, re.M)
#list of all lines that contains server interface word
client_iface=re.findall( r'<client_iface.*', config, re.M)
diface = {}
for i in range(len(server_iface)):
    siface = re.search(r'enp.*', server_iface[i]).group()[:-2] 
    #extract the interface name from the line
    ciface=re.search(r'enp.*', client_iface[i]).group()[:-3]
    diface[siface] = ciface

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description="Parsing xml arguments")
ap.add_argument("-s", "--server_ip", help="change server ip value")
ap.add_argument("-c", "--client_ip", help="change client ip value")
ap.add_argument("-i", "--iface", nargs=2, help="change client ip value")

args = ap.parse_args()

if args.server_ip:
    new_ip = vars(args)["server_ip"]
    if(valid_ip(new_ip)):
        update_file(server_ip, new_ip)
        server_ip = new_ip
    else:
        print "invalid ip"
		
	
if args.client_ip:
    new_ip = vars(args)["client_ip"]
    if(valid_ip(new_ip)):
        update_file(server_ip, new_ip)
        client_ip = new_ip
    else:
        print "invalid ip"

if args.iface:
    key = vars(args)["iface"][0]
    new_value = vars(args)["iface"][1]
    update_file(diface[key], new_value)
    diface[key] = new_value
	

print "server_ip: ", server_ip
print "client_ip: ", client_ip
print "{:<15} {:<15}".format('server_iface','client_iface')
for item in diface.items():
    print "{:<15} {:<15}".format(item[0], item[1])

