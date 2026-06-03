# Project Description

This project is my Maturitätsarbeit. Its final goal is to be able to generate climbing routes given a set of restrictions and demands (detailed in the file Climbing.md).
Here is a very short breakdown of my goals for the project and a general plan: (last updated 31.05.26) 

## Level 0: Basic framework complete

Deadline: End of school year (Mid-July)

The program should have a basic set of dataclasses (Holds, Walls and Routes) and databanks with some options. Given this data it should be able to list out this information on demand and add new data to the right databank. In addition the program should be able to calculate within the given restrictions a group of objects which could be used to create a route with the predetermined difficulty range.

## Level 1: Creation of proper routes

Deadline: Mid-September

The program at this point should be able to list where the holds on the wall go as (x/y) coordinates (third dimension not yet taken into account, as walls are still themselves 2D). In order to do this the program will have an algorithm that generates possible distances between hand holds. 
In addition to this feature the program should also be able to place footholds underneath handholds where necessary. 

## Level 2: UI

Deadline: Mid-October 

At this stage the program should have a user interface that is capable of displaying the generated routes, as well as saving them. The possibility of adding specific demands such as jumps (i.e exceptionally longer distance between two holds) should also be functional. The UI and 2D modelling will most likely be done by Marimo Notebook. 

## Level 3: Extra

Deadline: December

If all goes according to plan, additional features will be added: 

* 3D Walls (z component taken into account)
* Volumes / uneven surfaces on the walls 
* complicated demands such as cruxes, edges, heelhooks, kneebars...
* different route settings for different climber sizes (children, very short/tall adults...)  ) 