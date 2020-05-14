# Static Timing Analyzer
A Logic Circuit Static Timing Analyzer Implemented in Python 🔌 ⚡ (2018)

The analyzer is implemented over several parts.
It functions on Gate Level Netlists obtained from custom designs created in Verilog. 
Using as inputs a SCL JSON file and JSON files containing Timing Constraints, Net Capacitances, and Clock Skews, the system:
* Fetches the module name from the GUI and finds it in the gate level netlist file
* Searches for each gate in the standard cell library (SCL)
* Determines if it is sequential or combinational
* Finds its output capacitance from the net capacitance file and the SCL, and its input slew from the SCL (first gate assumed to have max input slew) to find each timing arc for either rising or falling using the gate’s unate
* Adds the gate as a node in the DAG, and stores its delay as the maximum delay of all the timing arcs (A-Y, B-Y, C-Y or CLK-Q)

## If the logic is combinational, it:
* Adds the delay of the gate to the Tpd of the current path and to the total delay of the current path

## If the logic is sequential, it:
* Calculates TCQ as the timing arc CLK-Q as mentioned in step 5
* Calculates Tskew using the clock skews file by finding the clock that has the same ID as the current flip flop and tracing a random path to that clock through the clock tree generated based on the module chosen
* Finds Tsetup and Thold using transition time of pin D (input slew) and transition time of pin CLK (Tskew), chooses rising or falling based on triggering edge
* Adds the delay of the gate to the total delay of the current path
## Finally, it:
* For each path, it identifies its type using the current gate’s type and the previous gates’ types
* Adds edges between nodes in DAG based on wire connections
* Calculates arrival and required time and slack for each node
* Finds critical path by examining the total delay of each identified path and taking the maximum
* Checks for setup and hold violations using Tcycle from the timing constrains file
* Displays the report and DAG in the GUI
