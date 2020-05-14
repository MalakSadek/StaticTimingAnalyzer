import json
from pprint import pprint
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from array import array
delay = [0] * 93
totaldelay = 0
path = ["0"] * 93
pathdelay = [0] * 93
G = nx.Graph();
cellkey = "$abc$26871$auto$blifparse.cc:346:parse_blif$";
cellindex = 26872;
DFFkey = "$auto$simplemap.cc:420:simplemap_dff$";
DFFindex = 14505;
totalpath = ["0"] * 153
arc1 = 0;
arc2 = 0;
arc3 = 0;
a = 0;
b = 0;
k = 0;
f = 0;
count = 0;
with open('/Users/malaksadek/Desktop/GateLevelNetlists.json') as data_file:    
    data = json.load(data_file)
    
with open('/Users/malaksadek/Desktop/SCL.json') as data_file:
    SCL = json.load(data_file)

for y in range(0,63):
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    max_x = 0;
    y = 1;
    capacitancecounter = 0;
    gatecapacitance = 0;
    tablecounterr = 0;
    tablecounterf = 0;
    for x in range(0,37):
        k = 0;
        capacitancecounter = capacitancecounter+1;
        if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"] == SCL["cells"][x]["name"]:
            #print("\n Found in library! Gate Name: " + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"]);
            #print("\n Timing Arc A-Y: ");
            gatecapacitance = 0.015;
            max_xr = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["max_x"];
            max_xf = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["max_x"];
            
            while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["points"][k]) or str(max_xr) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["points"][k]):
                   tablecounterr = tablecounterr + 1;
                   k = k + 1;
            k = 0;
            while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["points"][k]) or str(max_xf) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["points"][k]):
                   tablecounterf = tablecounterf + 1;
                   k = k + 1;
            
            arc1= max(((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["targets"][tablecounterr-1]), (SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["targets"][tablecounterf-1])));
            #print(arc1);
            tablecounterr = 0;
            tablecounterf = 0;
            k = 0;
            if "2" in SCL["cells"][x]["name"]:
                  #print("\n Timing Arc B-Y: ");
                  gatecapacitance = 0.4;      
                  while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["points"][k]) or str(max_xr) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["points"][k]):
                      tablecounterr = tablecounterr + 1;
                      k = k + 1;
                  k = 0;
                  while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["points"][k]) or str(max_xf) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["points"][k]):
                      tablecounterf = tablecounterf + 1;
                      k = k + 1;
                  arc2= max(((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["targets"][tablecounterr-1]), (SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["targets"][tablecounterf-1])));
                  #print(arc2);
                  tablecounterr = 0;
                  tablecounterf = 0;         
            #print("\n Delay for this node: ");
            #print(max(arc1,arc2));
    
    delay[y] = max(arc1,arc2);
    totaldelay = totaldelay+delay[y];
    pathdelay[f] = pathdelay[f] + delay[y];
    G.add_node(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"])
    
    if count == 0:
        path[f] = "\n Path starting point: " + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"] + "\n"
        totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"]
        print("HEYYYYY")
    elif count == 93:
        path[f] = path[f] + "\n Path ending point: " + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"] + path[f] + "\n Type: Input to Output \n Path Delay: " + str(pathdelay[f])
        totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"]
        f = f+1  
    else: 
        totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"] +  " -> "   
    
    count = count+1;

count = 0; 
tablecounterr = 0;
tablecounterf = 0;     
for y in range(0,31):
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    for x in range(0,37):
        k = 0;
        if data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] == SCL["cells"][x]["name"]:
            #print("\n Found in library! Gate Name: " + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"]);
            max_xr = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["max_x"];
            max_xf = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["max_x"];
            print (max_xr)
            #print("\n Timing Arc D-Q: ");
            gatecapacitance = 0.015;
           
            while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["points"][k]) or str(max_xr) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["points"][k]):
                   tablecounterr = tablecounterr + 1;
                   k = k + 1;
            k = 0;
            while str(gatecapacitance) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["points"][k]) or str(max_xf) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["points"][k]):
                   tablecounterf = tablecounterf + 1;
                   k = k + 1;
            arc1= max((SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["targets"][tablecounterr]), (SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["targets"][tablecounterf]));
            tablecounterr = 0;
            tablecounterf = 0;
            #print("\n Delay for this node: ");
            #print(arc1);   
    delay[y] = arc1;
    totaldelay = totaldelay + delay[y];
    pathdelay[f] = pathdelay[f] + delay[y];
    G.add_node(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"])

    if count == 0:
        if path[f] == "0":
            path[f] = "\n Path starting point: " + data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+y))]["type"] + "\n";
            totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " -> "
        else:
            path[f] = path[f] + "\n Path ending point: " + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + "\n Type: Input to Register \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " -> "
            f = f+1
    if count == 30:  
            path[f] = path[f] + "\n Path ending point: " + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"]+ "\n Type: Register to Output \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " -> "
            f = f+1
    elif "DFF" in data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"]:
            if path[f] == "0":
                path[f] = "\n Path starting point: " + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + "\n";
                totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " -> " 
            else:
                path[f] =  path[f] + "\n Path ending point: " + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + "\n Type: Register to Register \n Path Delay: " + str(pathdelay[f])
                totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " -> "
                f = f+1
    else:
        totalpath[f] = totalpath[f] + data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+y))]["type"] + " -> "    
    count = count + 1;
    
d = 0
k = 0
count = 0;
for i in range(0,63):
    count = count + 1;
    if k <= 30:
        k=k+1
    for j in range(0,63):
        if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+i))]["connections"]["A"] == data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
            G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
        if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+k))]["connections"]["A"] == data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+d))]["connections"]["D"]:
            G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
            if d <= 30: d=d+1
        if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
            G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
        if data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+k))]["connections"]["Q"] == data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
            G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
            if d <= 30: d=d+1
        if "2" in data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+i))]["type"]:
            if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
                G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
            if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+d))]["connections"]["D"]:
                G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
                if d <= 30: d=d+1
        if "2" in data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["type"]:
            if data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
                G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
            if data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+k))]["connections"]["Q"] == data["modules"]["dflipflop"]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
                G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"]["dflipflop"]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
                if d <= 30: d=d+1

count = 0;
for i in range(0,31):
    count = count + 1;
    for j in range(0,31):
        if data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+i))]["connections"]["D"] == data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+j))]["connections"]["Q"]:
            G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][DFFkey+str(DFFindex+i)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"]["dflipflop"]["cells"][DFFkey+str(DFFindex+(j))]["type"]+" Delay: "+str(totaldelay[y]))
        if data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+i))]["connections"]["Q"] == data["modules"]["dflipflop"]["cells"][DFFkey+str((DFFindex+j))]["connections"]["D"]:
            G.add_edge(str(count)+data["modules"]["dflipflop"]["cells"][DFFkey+str(DFFindex+j)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"]["dflipflop"]["cells"][DFFkey+str(DFFindex+(i))]["type"]+" Delay: "+str(totaldelay[y]))
f=0;

for i in range(0,93):
    if path[i] != "0":
           print(path[i])
