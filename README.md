# COL864-Task-Planning
Assignment for the COL864 - Special topics in AI (Robotics) course at IITD.
Objective: Gaining exposure to a virtual environment with a simulated robot agent that can interact with objects in the scene. Formulating and solving a symbolic planning problem. 

## Simulation Environment
The simulation is based on PyBullet simulator with a husky robot and UR5 manipulator arm. The robot can preform simple actions like move, pick, drop, open/close doors and push objects. 

## State representaiton
A state is a python dictionary of the form: 
```
{'grabbed': '', 'fridge': 'Close', 'inside': [], 'on': [], 'close': []}
```
* state\['grabbed'\] - object currently grabbed by the robot
* state\['fridge'\] - fridge state in (Open/Close)
* state\['inside'\] - consists of pairs of objects (a,b) where object a is inside object b
* state\['on'\] - consists of pairs of objects (a,b) where object a is on top of object b
* state\['close'\] - list of objects close to the robot

## Action types
To execute a plan in the simulation environment you can use the following functions:
* \[moveTo, object\] - moves robot close to object
* \[pick, object\] - picks the specified object
* \[drop, destination\] - drops a grabbed object to destination object
* \[changeState, object, state\] - changes the state of an object (open or close)
* \[pushTo, object, destination\] - pushes object close to the desitnation object

A  plan is a list of the above mentioned actions with objects in the set - (apple, orange, banana, table, table2, box, fridge, tray, tray2). You can input a plan to the *execute()* function which outputs a pair (plan success, final state after plan execution).

## Problem Statement
You are expected to build a planner for robots in diverse environments with complex interactions. You need to develop an approximate environment model which is able to change the state corresponding to an input action with action feasibility checking. The environment model needs to be implemented in *changeState()* and *checkAction()* functions in *environment.py* file. A standard goal checking function has been implemented which is the output of the *checkGoal()* function. The planner should be implemented in the *getPlan()* function in *planner.py* file.

The default goal in the simulator is to put all fruits in the fridge (and keep the fridge closed).


## Setup
To setup the PyBullet (physics engine) environment please run the following (assuming python3):
```
pip install -r requirements.txt
```

## Run
To run a plan with the given API and visualize on the simulator run the following command:
```
python planner.py --world jsons/home_worlds/world_home0.json
```
