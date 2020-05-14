import json
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from array import array
delay = [0] * 7
totaldelay = 0
path = ["0"] * 7
pathdelay = [0] * 7
G = nx.Graph();
DFFkey = "$auto$simplemap.cc:420:simplemap_dff$";
DFFindex = 48;

arc1 = 0;
arc2 = 0;
arc3 = 0;
a = 0;
b = 0;
count = 0;
with open('/Users/malaksadek/Desktop/GateLevelNetlists.json') as data_file:    
    data = json.load(data_file)
    
with open('/Users/malaksadek/Desktop/SCL.json') as data_file:
    SCL = json.load(data_file)
f = 0
 
for y in range(0,7):
    count = count + 1;
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    for x in range(0,37):
        if data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+y))]["type"] == SCL["cells"][x]["name"]:
            pprint("Found in library!");
            pprint("Timing Arc D-Q: ");
            arc1=((SCL["cells"][x]["properties"]["pins"]["CLK"]["internal_power"]["any"]["rise_power"]["targets"][5])+(SCL["cells"][x]["properties"]["pins"]["CLK"]["internal_power"]["any"]["fall_power"]["targets"][5]))/2;
            pprint("Delay for this node: ");
            pprint(arc1);   
    delay[y] = max(arc1,arc2,arc3);
    totaldelay = totaldelay + delay[y];
    pathdelay[f] = pathdelay[f] + delay[y];
    f=f+1;
    G.add_node(str(count)+data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+y))]["type"])


#count = 0;
#for i in range(0,7):
#    count = count + 1;
#    for j in range(0,7):
#        if data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+i))]["connections"]["D"] == data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+j))]["connections"]["Q"]:
#            G.add_edge(str(count)+data["modules"]["shift"]["cells"][DFFkey+str(DFFindex+i)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"]["shift"]["cells"][DFFkey+str(DFFindex+(j))]["type"]+" Delay: "+str(totaldelay[y]))
#        if data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+i))]["connections"]["Q"] == data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+j))]["connections"]["D"]:
#            G.add_edge(str(count)+data["modules"]["shift"]["cells"][DFFkey+str(DFFindex+j)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"]["shift"]["cells"][DFFkey+str(DFFindex+(i))]["type"]+" Delay: "+str(totaldelay[y]))
f=0;
count = -1;
for y in range(0,7):
    count = count+1;
    if count == 6:
        if "48" not in data["modules"]["shift"]["cells"][DFFkey+str((DFFindex))]:
            path[f] = path[f] + " **Type: Register to Output, Path Delay: " + str(pathdelay[f])
        elif "48" in data["modules"]["shift"]["cells"][DFFkey+str((DFFindex))]:
            path[f] = path[f] + " **Type: Input to Output, Path Delay: " + str(pathdelay[f])
            f = f+1
    elif "DFF" in data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+y))]["type"]:
        if "48" not in DFFkey+str((DFFindex+y)):
            path[f] = path[f] + data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " **Type: Register to Register, Path Delay: " + str(pathdelay[f])
            f = f+1
        elif "48" in DFFkey+str((DFFindex+y)):
            path[f] = path[f] + data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " **Type: Input to Register, Path Delay: " + str(pathdelay[f])
            f = f+1
    else: 
        path[f] = path[f] + data["modules"]["shift"]["cells"][DFFkey+str((DFFindex+y))]["type"] +" Delay: "+ str(delay[y]) + " -> "    

for i in range(0,7):
    if path[i] != "0":
           pprint(path[i])