import json
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from array import array
delay = [0] * 153
totaldelay = 0
path = ["0"] * 153
pathdelay = [0] * 153
G = nx.Graph();
cellkey = "$abc$26562$auto$blifparse.cc:346:parse_blif$";
cellindex = 26563;
totalpath = ["0"] * 153
arc1 = 0;
arc2 = 0;
arc3 = 0;
a = 0;
b = 0;
count = 0;
k = 1;
f = 0;

with open('/Users/malaksadek/Desktop/GateLevelNetlists.json') as data_file:    
    data = json.load(data_file)
    
with open('/Users/malaksadek/Desktop/SCL.json') as data_file:
    SCL = json.load(data_file)

for y in range(0,153):
    count = count + 1;
    arc1 = 0;
    arc2 = 0;
    a = a+1;
    b = b+1;
    max_x = 0;
    capacitancecounter = 0;
    gatecapacitance = 0;
    tablecounterr = 0;
    tablecounterf = 0;
    for x in range(0,37):
        k = 1;
        capacitancecounter = capacitancecounter+1;
        if data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] == SCL["cells"][x]["name"]:
            print("\n Found in library! Gate Name: " + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]);
            print("\n Timing Arc A-Y: ");
            gatecapacitance = 0.015;
            max_xr = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["max_x"];
            max_xf = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["max_x"];
                        
            while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["points"][k]) or str(max_xr) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["points"][k]):
                   tablecounterr = tablecounterr + 1;
                   k = k + 1;
            k = 1;
            while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["points"][k]) or str(max_xf) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["points"][k]):
                   tablecounterf = tablecounterf + 1;
                   k = k + 1;
            
            arc1= max(((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["targets"][tablecounterr-1]), (SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["targets"][tablecounterf-1])));
            print(arc1);
            tablecounterr = 0;
            tablecounterf = 0;
            k = 1;
            if "2" in SCL["cells"][x]["name"]:
                  print("\n Timing Arc B-Y: ");
                  gatecapacitance = 0.4;      
                  while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["points"][k]) or str(max_xr) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["points"][k]):
                      tablecounterr = tablecounterr + 1;
                      k = k + 1;
                  k = 1;
                  while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["points"][k]) or str(max_xf) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["points"][k]):
                      tablecounterf = tablecounterf + 1;
                      k = k + 1;
                  arc2= max(((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["targets"][tablecounterr-1]), (SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["targets"][tablecounterf-1])));
                  pprint(arc2);
                  tablecounterr = 0;
                  tablecounterf = 0;
            print("\n Delay for this node: ");
            print(max(arc1,arc2));
    delay[y] = max(arc1,arc2);
    totaldelay = totaldelay+delay[y];
    pathdelay[f] = pathdelay[f] + delay[y];
    G.add_node(str(count)+data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]);
    
   
for i in range(0,153):
    count = count + 1;
    for j in range(0,153):
        if data["modules"]["Adder"]["cells"][cellkey+str((cellindex+i))]["connections"]["A"] == data["modules"]["Adder"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
            G.add_edge(str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
        if data["modules"]["Adder"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["Adder"]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
            G.add_edge(str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
        if "2" in data["modules"]["Adder"]["cells"][cellkey+str((cellindex+i))]["type"]:
            if data["modules"]["Adder"]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"]["Adder"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
                G.add_edge(str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
        if "2" in data["modules"]["Adder"]["cells"][cellkey+str((cellindex+j))]["type"]:
            if data["modules"]["Adder"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["Adder"]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
                G.add_edge(str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["Adder"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
count = -1;
for y in range(0,153):
    count = count+1;
    if count == 0:
        path[f] = "\n Path starting point: " + path[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]
        totalpath[f] = totalpath[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]
    elif count == 152:
        if "DFF" in path[f]:
            path[f] = "\n Path ending point: " + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] + path[f] + "\n Type: Register to Output \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]
            f = f+1
        elif "DFF" not in path[f]:
            path[f] = "\n Path ending point: " + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] + path[f] + "\n Type: Input to Output \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]
            f = f+1
    elif "DFF" in data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]:
        if "DFF" in path[f]:
            path[f] = "\n Path ending point: " + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] + path[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] + "\n Type: Register to Register \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]
            f=f+1
        elif "DFF" not in path[f]:
            path[f] = "\n Path ending point: " + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] + path[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] + "\n Type: Input to Register, \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"]
            f = f+1    
    else: 
        totalpath[f] = totalpath[f] + data["modules"]["Adder"]["cells"][cellkey+str((cellindex+y))]["type"] +  " -> "   
    

count = 0;
#for i in range(0,153):
    #if path[i] != "0":
           #print(path[i])
           #print(totalpath[i])