# Distribution network planning

The traveling salesman problem (TSP) is a popular starting point to distribution network planning and route optimization in logistice. It is combined with the Center of Gravity (CoG) problem to provide a complete solution for a distribution network design problem. 

## Prerequisites 

Software development kits (SDK):

[Python](https://www.python.org/downloads/) 

and a text editor with syntax highlighting, e.g.:

[Notepad++](https://notepad-plus-plus.org/downloads/)

## Local construction process:

1. Check Python SDK (`python --version`)

2. `git clone https://github.com/romyg7/dnp.git`
  
3. `cd dnp`

4. run the chosen source file

## Source explanation

CoG.py - center of gravity (concept)
CoG2.py - center of gravity calculation with realistic coordinates
salesman.py - TSP problem (concept)
salesman_CoG.py - TSP based on CoG and euclid (aerial) distances
salesman_CoG2.py - TSP based on CoG, road distances and fuel consumption of trucks
