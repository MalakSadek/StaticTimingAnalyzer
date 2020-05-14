#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:13:43 2017

@author: malaksadek
"""
from random import randint
import json
import networkx as nx

with open('/Users/malaksadek/Desktop/GateLevelNetlists.json') as data_file:    #Getting the gate level netlist
    data = json.load(data_file)
    
with open('/Users/malaksadek/Desktop/SCL.json') as data_file:                  #Getting the standard cell library
    SCL = json.load(data_file)

with open('/Users/malaksadek/Desktop/NetCapacitance.json') as data_file:       #Getting the net capacitance file
    netcapacitance = json.load(data_file)
    
with open('/Users/malaksadek/Desktop/ClockSkews.json') as data_file:           #Getting the clock skews file
    skews = json.load(data_file)
    
with open('/Users/malaksadek/Desktop/TimingConstraints.json') as data_file:    #Getting the timing constraints file
    constraints = json.load(data_file)

modulename = raw_input("Modules Available: Adder, MuxN, mux2, idmem, regfile, dflipflop, div, shift \nPlease enter a module name to test: \n") #choosing a module to produce a report for

numberofgates = 0
for y in data["modules"][modulename]["cells"]:   #This calculates the number of gates in the module
    numberofgates = numberofgates + 1

delay = [0] * numberofgates         #stores the delay of each gate/node
path = ["0"] * numberofgates        #stores the starting and ending points of each path in the module, the path's type, and its delay (input to output, input to register, register to register, register to output)
pathdelay = [0] * numberofgates     #stores the total delay of each path
G = nx.Graph();                     #stores the DAG
totalpath = ["0"] * numberofgates   #stores all the gates that make up each path
arc1 = 0;
arc2 = 0;

a = 0;
b = 0;
k = 0;
f = 0;
outputcapr = 0;
outputcapf = 0;
count = 0;
inputslew = 0;    
Y = 0;

TCycle = constraints["clock period"] - constraints["uncertainty"]
TSkew = [0] * numberofgates
TSetup = [0] * numberofgates
THold = [0] * numberofgates
TCQ = [0] * numberofgates
Setup = [0] * numberofgates
Hold = [0] * numberofgates
RT = [0] * numberofgates
AT = [0] * numberofgates
slack = [0] * numberofgates
inputdelay = constraints["constraints"][randint(0,9)]["input_delay"]
outputdelay = constraints["constraints"][randint(0,9)]["output_delay"]

for y in data["modules"][modulename]["cells"]:
    arc1 = 0;
    arc2 = 0;
    arc3 = 0;
    a = a+1;
    b = b+1;
    max_x = 0;
    capacitancecounter = 0;
    gatecapacitanceA = 0;
    gatecapacitanceB = 0;
    tablecounterr = 0;
    tablecounterf = 0;
    capacitanceoptionsA = [0]*5;
    capacitanceoptionsB = [0]*5;
    inputslewoptionsA = [0]*5;
    inputslewoptionsB = [0]*5;
    
    if "DFF" not in data["modules"][modulename]["cells"][y]["type"] and "LATCH" not in data["modules"][modulename]["cells"][y]["type"]:
        for x in range(0,37):
            k = 0;
            for q in range (0,37):
               if data["modules"][modulename]["cells"][y]["type"] == netcapacitance["cells"][q]["name"]:
                  capacitance = netcapacitance["cells"][q]["capacitance"];
            capacitancecounter = capacitancecounter+1;
            if data["modules"][modulename]["cells"][y]["type"] == SCL["cells"][x]["name"]:
                print("\nFound in library! Gate Name: " + data["modules"][modulename]["cells"][y]["type"]);
                print("\nTiming Arc A-Y: ");
                for i in range (0,5):
                    capacitanceoptionsA[i] = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["y_values"][i];
                    inputslewoptionsA[i] = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["x_values"][i];
                gatecapacitanceA = SCL["cells"][x]["properties"]["pins"]["A"]["capacitance"] + float(capacitance);
                minimum = 1000;
                index = 0;
                for i in range (0,5):
                    difference = abs(gatecapacitanceA - capacitanceoptionsA[i]);
                    if difference < minimum:
                        minimum = difference;
                        index = i;
                gatecapacitanceA = capacitanceoptionsA[index];
                max_xr = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["max_x"];
                max_xf = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["max_x"];
                
                if count == 0:
                    outputcapacitancef = max_xf;
                    outputcapacitancer = max_xr;
                    inputslew = 1.2;
                else:
                    if "DFF" not in SCL["cells"][x]["name"] and "LATCH" not in SCL["cells"][x]["name"]:
                        while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["points"][k]):
                            tablecounterr = tablecounterr + 1;
                            k = k + 1;
                        outputcapacitancer = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["targets"][tablecounterr-1];
                        k = 0;
                        while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["points"][k]):
                            tablecounterf = tablecounterf + 1;
                            k = k + 1;
                        outputcapacitancef = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["targets"][tablecounterf-1];
                    else:
                        while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]):
                            tablecounterr = tablecounterr + 1;
                            k = k + 1;
                        outputcapacitancer = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["targets"][tablecounterr-1];
                        k = 0;
                        while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]):
                            tablecounterf = tablecounterf + 1;
                            k = k + 1;
                        outputcapacitancef = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["targets"][tablecounterf-1];
                
                inputslew = max(outputcapacitancer, outputcapacitancef);
                tablecounterr = 0;
                tablecounterf = 0;
                minimum = 1000;
                index = 0;
                k = 0;
                for i in range (0,5):
                    difference = abs(inputslew - inputslewoptionsA[i]);
                    if difference < minimum:
                        minimum = difference;
                        index = i;
                inputslew = inputslewoptionsA[index];
                while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["points"][k]):
                    tablecounterr = tablecounterr + 1;
                    k = k + 1;
                k = 0;
                
                while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["points"][k]):
                       tablecounterf = tablecounterf + 1;
                       k = k + 1;
                       
                arc1= max(((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["targets"][tablecounterr-1]), (SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["targets"][tablecounterf-1])));
                print(arc1);
                tablecounterr = 0;
                tablecounterf = 0;
                k = 0;
                if "2" in SCL["cells"][x]["name"]:
                      print("\nTiming Arc B-Y: ");
                      
                      for i in range (0,5):
                          capacitanceoptionsB[i] = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["y_values"][i];
                          inputslewoptionsB[i] = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["x_values"][i];
                      gatecapacitanceB = SCL["cells"][x]["properties"]["pins"]["B"]["capacitance"] + float(capacitance);
                      minimum = 1000;
                      index = 0;
                      for i in range (0,5):
                          difference = abs(gatecapacitanceB - capacitanceoptionsB[i]);
                          if difference < minimum:
                              minimum = difference;
                              index = i;
                      gatecapacitanceB = capacitanceoptionsB[index];
                      
                      if count == 0:
                          outputcapacitancef = max_xf;
                          outputcapacitancer = max_xr;
                      else:
                          if "DFF" not in SCL["cells"][x]["name"] and "LATCH" not in SCL["cells"][x]["name"]:
                              while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["points"][k]):
                                  tablecounterr = tablecounterr + 1;
                                  k = k + 1;
                              outputcapacitancer = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["rise_transition"]["targets"][tablecounterr-1];
                              k = 0;
                              while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_fall"]["points"][k]):
                                  tablecounterf = tablecounterf + 1;
                                  k = k + 1;
                              outputcapacitancef = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["fall_transition"]["targets"][tablecounterf-1];
                          else:
                              while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]):
                                  tablecounterr = tablecounterr + 1;
                                  k = k + 1;
                              outputcapacitancer = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["targets"][tablecounterr-1];
                              k = 0;
                              while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]):
                                  tablecounterf = tablecounterf + 1;
                                  k = k + 1;
                              outputcapacitancef = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["targets"][tablecounterf-1];
                
                      inputslew = max(outputcapacitancer, outputcapacitancef);
                      tablecounterr = 0;
                      tablecounterf = 0;
                      minimum = 1000;
                      index = 0;
                      k = 0;
                      for i in range (0,5):
                          difference = abs(inputslew - inputslewoptionsB[i]);
                          if difference < minimum:
                              minimum = difference;
                              index = i;
                      inputslew = inputslewoptionsA[index];
                      while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["points"][k]):
                          tablecounterr = tablecounterr + 1;
                          k = k + 1;
                      k = 0;
                      tablecounterr = 0;
                      tablecounterf = 0;          
                      while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["points"][k]):
                          tablecounterr = tablecounterr + 1;
                          k = k + 1;
                      k = 0;
                      while str(gatecapacitanceB) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_fall"]["points"][k]):
                          tablecounterf = tablecounterf + 1;
                          k = k + 1;
                      arc2= max(((SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_rise"]["targets"][tablecounterr-1]), (SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["B"]["cell_fall"]["targets"][tablecounterf-1])));
                      print(arc2);
                tablecounterr = 0;
                tablecounterf = 0;         
        print("\nDelay for this node: ");
        print(max(arc1,arc2));
        
        delay[Y] = max(arc1,arc2);
        totaldelay = totaldelay+delay[Y];
        pathdelay[f] = pathdelay[f] + delay[Y];
        G.add_node(data["modules"][modulename]["cells"][y]["type"])
        #if y != 0:
            #G.add_edge(G.node[Y],G.node[Y-1], weight=delay[Y])

    else:  
            tablecounterr = 0;
            tablecounterf = 0; 
            arc1 = 0;
            arc2 = 0;
            arc3 = 0;
            a = a+1;
            b = b+1;
            
            TSkew[Y] = skews["skews"][randint(0,9)]["skew"]
            TCQ[Y] = constraints["constraints"][randint(0,9)]["TCQ"]
            THold[Y] = constraints["constraints"][randint(0,9)]["THold"]
            TSetup[Y] = constraints["constraints"][randint(0,9)]["TSetup"]
            print("TSkew: "+ str(TSkew[Y]) + "TCQ: "+ str(TCQ[Y]) +" THold: "+ str(THold[Y]) +" TSetup: " + str(TSetup[Y]))

            if inputslew != 0.06 and inputslew != 0.24 and inputslew != 0.48 and inputslew != 0.9 and inputslew != 1.2 and inputslew != 1.8:
                inputslew = 1.8;

            for x in range(0,37):
                k = 0;
                for g in range (0,37):
                    if data["modules"][modulename]["cells"][y]["type"] == netcapacitance["cells"][g]["name"]:
                        capacitance = netcapacitance["cells"][g]["capacitance"];
                
                if data["modules"][modulename]["cells"][y]["type"] == SCL["cells"][x]["name"]:
                    print("\n Found in library! Gate Name: " + data["modules"][modulename]["cells"][y]["type"]);
                    max_xr = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["max_x"];
                    max_xf = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["max_x"];
                    print("\nTiming Arc Q-CLK: ");
                
                    for i in range (0,5):
                        capacitanceoptionsA[i] = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["y_values"][i];
                        inputslewoptionsA[i] = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["x_values"][i];
                    gatecapacitanceA = SCL["cells"][x]["properties"]["pins"]["Q"]["capacitance"] + capacitance;
                    
                    minimum = 1000;
                    index = 0;
                    for i in range (0,5):
                        difference = abs(gatecapacitanceA - capacitanceoptionsA[i]);
                        if difference < minimum:
                            minimum = difference;
                            index = i;
                    gatecapacitanceA = capacitanceoptionsA[index];
                                    
                    if count == 0:
                        outputcapacitancef = max_xf;
                        outputcapacitancer = max_xr;
                    else:
                        if "DFF" not in SCL["cells"][x]["name"] and "LATCH" not in SCL["cells"][x]["name"]:
                            tablecounterr = 0;
                            tablecounterf = 0;
                            k = 0;  
                            while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_rise"]["points"][k]):
                                tablecounterr = tablecounterr + 1;
                                k = k + 1;
                            outputcapacitancer = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["rise_transition"]["targets"][tablecounterr-1];
                            k = 0;
                            while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["cell_fall"]["points"][k]):
                                tablecounterf = tablecounterf + 1;
                                k = k + 1;
                            outputcapacitancef = SCL["cells"][x]["properties"]["pins"]["Y"]["timing"]["A"]["fall_transition"]["targets"][tablecounterf-1];
                        else:
                            k = 0;  
                            tablecounterr = 0;
                            tablecounterf = 0;
                            while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]):
                                tablecounterr = tablecounterr + 1;
                                k = k + 1;
                            outputcapacitancer = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["rise_transition"]["targets"][tablecounterr-1];
                            k = 0;
                            while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]):
                                tablecounterf = tablecounterf + 1;
                                k = k + 1;
                            outputcapacitancef = SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["fall_transition"]["targets"][tablecounterf-1];
                
                    inputslew = max(outputcapacitancer, outputcapacitancef);
                    minimum = 1000;
                    index = 0;
                    k = 0;
                    for i in range (0,5):
                        difference = abs(inputslew - inputslewoptionsA[i]);
                        if difference < minimum:
                            minimum = difference;
                            index = i;
                    inputslew = inputslewoptionsA[index];
                    while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]):
                        tablecounterr = tablecounterr + 1;
                        k = k + 1;
                    k = 0;
                                          
                    while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["points"][k]):
                        tablecounterr = tablecounterr + 1;
                        k = k + 1;
                    k = 0;
                    
                    while str(gatecapacitanceA) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]) or str(inputslew) not in str(SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["points"][k]):
                        tablecounterf = tablecounterf + 1;
                        k = k + 1;
                    
                    arc1= max((SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_rise"]["targets"][tablecounterr]), (SCL["cells"][x]["properties"]["pins"]["Q"]["timing"]["CLK"]["cell_fall"]["targets"][tablecounterf]));
                    tablecounterr = 0;
                    tablecounterf = 0;
                    print("\n Delay for this node: ");
                    print(arc1);   
            delay[Y] = arc1;
            totaldelay = totaldelay + delay[Y];
            pathdelay[f] = pathdelay[f] + delay[Y];
            G.add_node(str(count)+data["modules"][modulename]["cells"][y]["type"])
                
            #if y != 0:
               #G.add_edge(data["modules"][modulename]["cells"][Y]["type"], data["modules"][modulename]["cells"][Y-1]["type"], weight=delay[y])
    
    
    
    if count == 0:
            path[f] = "\n Path starting point: " + data["modules"][modulename]["cells"][y]["type"] + "\n"
            totalpath[f] = data["modules"][modulename]["cells"][y]["type"] + " -> "
    elif count == 92:
        if "DFF" not in totalpath[f] and "LATCH" not in totalpath[f]:
            path[f] = path[f] + "\n Path ending point: " + data["modules"][modulename]["cells"][y]["type"] + "\n Type: Input to Output \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"][modulename]["cells"][y]["type"]
            f = f+1  
        else:
            path[f] = path[f] + "\n Path ending point: " + data["modules"][modulename]["cells"][y]["type"] + "\n Type: Register to Output \n Path Delay: " + str(pathdelay[f])
            totalpath[f] = totalpath[f] + data["modules"][modulename]["cells"][y]["type"]
            f = f+1                  
    elif "DFF" in data["modules"][modulename]["cells"][y]["type"] or "LATCH" in data["modules"][modulename]["cells"][y]["type"]:
        if path[f] == "0":
            path[f] = "\n Path starting point: " + data["modules"][modulename]["cells"][y]["type"];
            totalpath[f] =  data["modules"][modulename]["cells"][y]["type"] + " -> "
        else:
            if "DFF" in totalpath[f] or "LATCH" in totalpath[f]:
                path[f] =  path[f] + "\n Path ending point: " + data["modules"][modulename]["cells"][y]["type"] + "\n Type: Register to Register \n Path Delay: " + str(pathdelay[f])
                totalpath[f] = totalpath[f] + data["modules"][modulename]["cells"][y]["type"]
                f = f+1
            else:
                path[f] =  path[f] + "\n Path ending point: " + data["modules"][modulename]["cells"][y]["type"] + "\n Type: Input to Register \n Path Delay: " + str(pathdelay[f])
                totalpath[f] = totalpath[f] + data["modules"][modulename]["cells"][y]["type"]
                f = f+1 
    else:
        totalpath[f] = totalpath[f] + data["modules"][modulename]["cells"][y]["type"] + " -> "    
    count = count + 1;      
    Y = Y + 1;

#for i in range(0,153):
#    count = count + 1;
#    for j in range(0,153):
#        if data["modules"][modulename]["cells"][cellkey+str((cellindex+i))]["connections"]["A"] == data["modules"][modulename]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
#            G.add_edge(str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#        if data["modules"][modulename]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"][modulename]["cells"][cellkey+str((cellindex+j))]["connections"]["A"]:
#            G.add_edge(str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))
#        if "2" in data["modules"][modulename]["cells"][cellkey+str((cellindex+i))]["type"]:
#            if data["modules"][modulename]["cells"][cellkey+str((cellindex+i))]["connections"]["B"] == data["modules"][modulename]["cells"][cellkey+str((cellindex+j))]["connections"]["Y"]:
#                G.add_edge(str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+i)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+(j))]["type"]+" Delay: "+str(delay[y]))
#        if "2" in data["modules"][modulename]["cells"][cellkey+str((cellindex+j))]["type"]:
#            if data["modules"][modulename]["cells"][cellkey+str((cellindex+i))]["connections"]["Y"] == data["modules"][modulename]["cells"][cellkey+str((cellindex+j))]["connections"]["B"]:
#                G.add_edge(str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+j)]["type"]+" Delay: "+str(delay[y]), str(count)+data["modules"][modulename]["cells"][cellkey+str(cellindex+(i))]["type"]+" Delay: "+str(delay[y]))    
#        if data["modules"][modulename]["cells"][DFFkey+str((DFFindex+i))]["connections"]["D"] == data["modules"][modulename]["cells"][DFFkey+str((DFFindex+j))]["connections"]["Q"]:
#            G.add_edge(str(count)+data["modules"][modulename]["cells"][DFFkey+str(DFFindex+i)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"][modulename]["cells"][DFFkey+str(DFFindex+(j))]["type"]+" Delay: "+str(totaldelay[y]))
#        if data["modules"][modulename]["cells"][DFFkey+str((DFFindex+i))]["connections"]["Q"] == data["modules"][modulename]["cells"][DFFkey+str((DFFindex+j))]["connections"]["D"]:
#            G.add_edge(str(count)+data["modules"][modulename]["cells"][DFFkey+str(DFFindex+j)]["type"]+" Delay: "+str(totaldelay[y]), str(count)+data["modules"][modulename]["cells"][DFFkey+str(DFFindex+(i))]["type"]+" Delay: "+str(totaldelay[y]))

for i in range (0, Y+1):
    if i == 0:
        AT[i] = delay[i]+inputdelay
        RT[Y-i] = TCycle-outputdelay-delay[Y-i]

    else:
        AT[i] = AT[i-1] + delay[i]
        RT[Y-i] = RT[(Y-i)+1] - delay[Y-i]

for i in range (0, Y):
    slack[i] = RT[i] - AT[i]
    print("\nFor node #" + str(i) + "\nRequired time: " + str(RT[i]) + "\nArrival time: " + str(AT[i]) + "\nSlack: " + str(slack[i]))
    if slack[i] < 0:
        print("Timing Violation at Node.")

f=0;
minimum = 0;
minindex = 0;
d = 0
for i in data["modules"][modulename]["cells"]:
    if path[d] != "0":
           print("\n Path Found! ID: " + str(d) + path[d])
           if pathdelay[d] > minimum:
               minimum = pathdelay[d];
               minindex = d;

           if TCycle < TCQ[d] + TSetup[d] + pathdelay[d] - TSkew[d]:
                   Setup[d] = 1
           if THold[d] > pathdelay[d] + TCQ[d] - TSkew[d]:
               Hold[d] = 1
    d = d + 1;       

d = 0;
flag = 0;
for i in data["modules"][modulename]["cells"]:
    if Setup[d] == 1:
        print("\nSetup Violation Detected!\n\nClock Period = " + str(TCycle) + " ns\nPath #" + str(d) + " Has a Tsetup of " + str(TSetup[d]) + " ns,\na TCQ of " + str(TCQ[d]) + " ns,\na Tskew of " + str(TSkew[d]) + " ns,\nand a Tpd of " + str(pathdelay[d]) + " ns. \nThere is a setup violation of " + str(abs(TCycle - TCQ[d] - TSetup[d] - pathdelay[d] + TSkew[d])) + " ns.")
        flag = 1;
    if Hold[d] == 1:
        print("\nHold Violation Detected!\n\nPath #" + str(d) + " Has a Thold of " + str(THold[d]) + " ns,\na TCQ of " + str(TCQ[d]) + " ns,\na Tskew of " + str(TSkew[d]) + " ns,\nand a Tpd of " + str(pathdelay[d]) + " ns. \nThere is a hold violation of " + str(abs(THold[d] - TCQ[d] - pathdelay[d] + TSkew[d])) + " ns.")
        flag = 1;
    d = d + 1
    
if flag == 0:
    print("No setup or hold violations detected! :)")

    print("Critical Path is: " + str(totalpath[minindex]) + "\nCritical Path Delay = "  + str(pathdelay[minindex]));
