# Concurrent Data Structures for 3d Simulation
Jefferson Van Buskirk, Ji Ho Choi, Jared Lee
jef@lehigh.edu, jic518@lehigh.edu, jrl222@lehigh.edu


## Overview
Bullet Physics SDK is an open source physics engine written in C++ that simulates collision detection, rigid body, and soft body dynamics. Inside this physics engine 
there is a data structure known as a BVH Tree that lacks multithreaded support. The overall goal of this project is to increate the performance of this data structure 
by changing the data strucutre or adding multithreaded support. In our first year we were not able to complete this so we have compiled what we were able to complete 
in this repository. 

## Executables
The executables directory contains simple example simulations to start to understand what Bullet is and does. The exectuables are created with both the internal BVT and 
the linked list that we created. They also have visualizer support to practice using the visualizer script. 

## Source Code
The source code directory contains commented versions of the original BVT to understand the functions/data types within it as well as our linked list implementation. The 
readme in this folder will get you up to speed on how to run the code with our linked list and how we implemented this linked list.

## Visualizer
The visualzier directory contains documentation and the scripts needed to run the visualizer. Inside the data structures we created functions that will write to a graph.txt file
that is then used in a python script to create images and then an avi video file. The readme in this directory will show you how to use this.
