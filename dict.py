#!/usr/bin/env python
from collections import defaultdict
from pprint import pprint
from xml.etree import ElementTree as ET

def etree_to_dict(etree):
    etree_dict = {etree.tag: {} if etree.attrib else None}
    #start whith dictionary {tag:None} ot {tag:{}} in case of existance of attribute
    children = list(etree)
    if children:
        ddict = defaultdict(list) #to group a sequence of key-value pairs into a dictionary
                               #in case of more than client interface under server interface tag
        for dc in map(etree_to_dict, children): #recursion
                                                #execute etree_to_dict for each item in children
                                                #reurn dictionary
            for key, value in dc.items():
                ddict[key].append(value)
        etree_dict = {etree.tag: {key:value[0] if len(value) == 1 else\
                                  value for key, value in ddict.items()}}#if more than one value 
                                                                         #with the same key, save
                                                                         #it as list
    if etree.attrib:#the attribute start with @
        etree_dict[etree.tag].update(('@' + key, value) for key, value in etree.attrib.items())
    if etree.text:
        text = etree.text.strip()
        if not (children or etree.attrib):
            etree_dict[etree.tag] = text
    return etree_dict

e = ET.XML('''
<configurations>
    <server_ip>10.0.10.2</server_ip>
    <client_ip>10.0.10.3</client_ip>
    <interfaces>
        <server_iface name="enp3s0f0">
            <client_iface name="enp21s0f0"/>
        </server_iface>
        <server_iface name="enp3s0f1">
            <client_iface name="enp21s0f1"/>
        </server_iface>
    </interfaces>
    <Branch>master</Branch>
</configurations>
''')
pprint(etree_to_dict(e))

