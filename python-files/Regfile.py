import json
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from array import array
delay = [0] * 4628
totaldelay = 0
path = ["0"] * 4628
pathdelay = [0] * 4628
G = nx.Graph();
cellkey = "$abc$32427$auto$blifparse.cc:346:parse_blif$";
cellindex = 32428;
DFFkey = "$auto$simplemap.cc:420:simplemap_dff$";
DFFindex = 7341;

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
for y in range(0,3669):
    count = count + 1;
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    for x in range(0,37):
        if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+y))]["type"] == SCL["cells"][x]["name"]:
            pprint("Found in library!");
            pprint("Timing Arc A-Y: ");
            arc1=((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["targets"][24])+(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["targets"][24]))/2;
            pprint(arc1);
            if "2" in SCL["cells"][x]["name"]:
                  pprint("Timing Arc B-Y: ");
                  arc2=((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["targets"][24])+(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_fall"]["targets"][24]))/2;
                  pprint(arc2);
            if "3" in SCL["cells"][x]["name"]:
                  pprint("Timing Arc C-Y: ");
                  arc3=((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["C"]["cell_rise"]["targets"][24])+(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["C"]["cell_fall"]["targets"][24]))/2;
                  pprint(arc3);           
            pprint("Delay for this node: ");
            pprint(max(arc1,arc2,arc3));
    delay[y] = max(arc1,arc2,arc3);
    totaldelay = totaldelay+delay[y];
    pathdelay[f] = pathdelay[f] + delay[y];
    G.add_node(str(count)+data["modules"]["regfile"]["cells"][cellkey+str((cellindex+y))]["type"])
    path[f] = path[f] + data["modules"]["regfile"]["cells"][cellkey+str((cellindex+y))]["type"] +" Delay: "+ str(delay[y]) + " -> "   
            
for y in range(0,959):
    count = count + 1;
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    for x in range(0,37):
        if data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+y))]["type"] == SCL["cells"][x]["name"]:
            pprint("Found in library!");
            pprint("Timing Arc D-Q: ");
            arc1=((SCL["cells"][x]["properties"]["pins"]["CLK"]["internal_power"]["any"]["rise_power"]["targets"][5])+(SCL["cells"][x]["properties"]["pins"]["CLK"]["internal_power"]["any"]["fall_power"]["targets"][5]))/2;
            pprint("Delay for this node: ");
            pprint(arc1);   
    delay[y] = max(arc1,arc2,arc3);
    totaldelay = totaldelay + delay[y];
    pathdelay[f] = pathdelay[f] + delay[y];
    f=f+1;
    G.add_node(str(count)+data["modules"]["regfile"]["cells"][cellkey+str((cellindex+y))]["type"])

#d = 0
#k = 0
#count = 0;
#for i in range(0,3669):
#    count = count + 1;
#    if k <= 958:
#        k=k+1
#    for j in range(0,3669):
#        if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["A"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
#            G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#        if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+k))]["connections"]["A"] == data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+d))]["connections"]["D"]:
#            G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#            if d <= 958: d=d+1
#        if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
#            G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#        if data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+k))]["connections"]["Q"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
#            G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#            if d <= 958: d=d+1
#       if "2" in data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["type"]:
#            if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
#                G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#            if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+d))]["connections"]["D"]:
#                G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#                if d <= 958: d=d+1
#        if "2" in data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["type"]:
#            if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
#                G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#            if data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+k))]["connections"]["Q"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
#                G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#                if d <= 958: d=d+1
#        if "3" in data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["type"]:      
#            if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["C"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
#                G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#            if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["C"] == data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+d))]["connections"]["D"]:
#                G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#                if d <= 958: d=d+1
#        if "3" in data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["type"]: 
#            if data["modules"]["regfile"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["C"]:
#               G.add_edge(str(count)+data["modules"]["div"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#            if data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+k))]["connections"]["Q"] == data["modules"]["regfile"]["cells"][cellkey+str((cellindex+j))]["connections"]["C"]:
#               G.add_edge(str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["regfile"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#               if d <= 958: d=d+1
#count = 0;
#for i in range(0,959):
#    count = count + 1;
#    for j in range(0,959):
#        if data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+i))]["connections"]["D"] == data["modules"]["div"]["cells"][DFFkey+str((DFFindex+j))]["connections"]["Q"]:
#            G.add_edge(str(count)+data["modules"]["regfile"]["cells"][DFFkey+str(DFFindex+i)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"]["regfile"]["cells"][DFFkey+str(DFFindex+(j))]["type"]+" Delay: "+str(totaldelay[y]))
#        if data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+i))]["connections"]["Q"] == data["modules"]["div"]["cells"][DFFkey+str((DFFindex+j))]["connections"]["D"]:
#            G.add_edge(str(count)+data["modules"]["regfile"]["cells"][DFFkey+str(DFFindex+j)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"]["regfile"]["cells"][DFFkey+str(DFFindex+(i))]["type"]+" Delay: "+str(totaldelay[y]))
f=0;
count = -1;
for y in range(0,959):
    count = count+1;
    if count == 958:
        if "0INVX1" not in path[f]:
            path[f] = path[f] + " **Type: Register to Output, Path Delay: " + str(pathdelay[f])
        elif "0INVX1" in path[f]:
            path[f] = path[f] + " **Type: Input to Output, Path Delay: " + str(pathdelay[f])
            f = f+1
    elif "DFF" in data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+y))]["type"]:
        if "0INVX1" not in path[f]:
            path[f] = path[f] + data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " **Type: Register to Register, Path Delay: " + str(pathdelay[f])
            f = f+1
        elif "0INVX1" in path[f]:
            path[f] = path[f] + data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " **Type: Input to Register, Path Delay: " + str(pathdelay[f])
            f = f+1
    else: 
        path[f] = path[f] + data["modules"]["regfile"]["cells"][DFFkey+str((DFFindex+y))]["type"] +" Delay: "+ str(delay[y]) + " -> "    

for i in range(0,4628):
    if path[i] != "0":
           pprint(path[i])

