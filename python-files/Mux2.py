import json
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from array import array
delay = [0] * 95
totaldelay = 0
path = ["0"] * 95
pathdelay = [0] * 95
G = nx.Graph();
cellkey = "$abc$32330$auto$blifparse.cc:346:parse_blif$";
cellindex = 32331;

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
for y in range(0,95):
    count = count + 1;
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    for x in range(0,37):
        if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"] == SCL["cells"][x]["name"]:
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
    G.add_node(str(count)+data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"]);
    
   
for i in range(0,95):
    count = count + 1;
    for j in range(0,95):
        if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["connections"]["A"] == data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
            G.add_edge(str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
        if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
            G.add_edge(str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
        if "2" in data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["type"]:
            if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
                G.add_edge(str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
        if "2" in data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["type"]:
            if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
                G.add_edge(str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
        if "3" in data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["type"]:      
            if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["connections"]["C"] == data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
                G.add_edge(str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
        if "3" in data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["type"]: 
            if data["modules"]["mux2"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["mux2"]["cells"][cellkey+str((cellindex+j))]["connections"]["C"]:
                G.add_edge(str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["mux2"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
count = -1;
for y in range(0,95):
    count = count+1;
    if count == 94:
        path[f] = path[f] + data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"]+" Delay: "+str(delay[y])
        if "DFF" in path[f]:
            path[f] = path[f] + " **Type: Register to Output, Path Delay: " + str(pathdelay[f])
        elif "DFF" not in path[f]:
            path[f] = path[f] + " **Type: Input to Output, Path Delay: " + str(pathdelay[f])
            f = f+1
    elif "DFF" in data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"]:
        if "DFF" in path[f]:
            path[f] = path[f] + data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"] + " **Type: Register to Register, Path Delay: " + str(pathdelay[f])
            f=f+1
        elif "DFF" not in path[f]:
            path[f] = path[f] + data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"] + " **Type: Input to Register, Path Delay: " + str(pathdelay[f])
            f = f+1    
    else: 
        path[f] = path[f] + data["modules"]["mux2"]["cells"][cellkey+str((cellindex+y))]["type"] +" Delay: "+ str(delay[y]) + " -> "   
    

count = 0;
for i in range(0,95):
    if path[i] != "0":
           pprint(path[i])