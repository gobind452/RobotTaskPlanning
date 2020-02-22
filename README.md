# COL864: Homework II
## Overview
This exercise concerns writing a symbolic planner for an agent (mobile manipulator) 
capable of interacting with objects in a virtual environment. 
The robot can perform a set of actions (move to, pick, place on, push to, open/close) 
which are described below. 
We assume a discrete world representation where the environment can be represented 
as a set of objects. 
The robot can move towards a given object or peform interactions 
with it. 
Some objects in the scene can have symbolic states. For example, a cupboard 
can be open or closed. 
We can assume that the robot can determine if an object is open or closed, 
if an object is inside or on top of an object or if it is close to an object 
of interest. 
Note that the agent does not know the semantics of when actions are applicable 
and what are their effects. Hence, cannot perform tasks such as moving an object 
to a goal location that requires chaining of actions. 
Hence, your objective is enable the robot with a 
task planner allowing it to perform tasks that require reasoning over a sequence of objects.  

## Simulation Environment and Agent Representation
### Virtual Environment 
The simulation is based on PyBullet simulator with a mobile manipulator (called Husky robot with a manipulator arm. 
The simulator consists of 10 world scenes and 5 different goals. 
A screenshot of the simulator appears below:
<div align="center">
<img src="https://github.com/shreshthtuli/COL864-Task-Planning/blob/master/screenshot.png" width="700" align="middle">
</div>
Note: All actions are symbolic and robot position is discretized by proximity to objects.

### World State 
The world state at any time instant is a python dictionary of the form: 
```
{'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': []}
```
Here, the symbols denote the following:
* state\['grabbed'\] - object currently grabbed by the robot
* state\['fridge'\] - fridge state in (Open/Close)
* state\['cupboard'\] - cupboard state in (Open/Close)
* state\['inside'\] - consists of pairs of objects (a,b) where object a is inside object b
* state\['on'\] - consists of pairs of objects (a,b) where object a is on top of object b
* state\['close'\] - list of objects close to the robot

### Action types
The robot can preform simple actions like move, pick, drop, open/close doors and push objects. 
To simulate a plan in the simulation environment you may use the following functions:
* \[moveTo, object\] - moves robot close to object
* \[pick, object\] - picks the specified object
* \[drop, destination\] - drops a grabbed object to destination object
* \[changeState, object, state\] - changes the state of an object (open or close)
* \[pushTo, object, destination\] - pushes object close to the destination object

A  plan is a sequence (python list) of the afore mentioned actions with objects 
in the set - (apple, orange, banana, table, table2, box, fridge, tray, tray2). 

You can input a plan to the *execute()* function which outputs a pair (plan success, final state after plan execution).

## Problem Statement
You are expected to build a planner for robots in diverse environments with complex interactions. You need to develop an approximate environment model which is able to change the state corresponding to an input action with action feasibility checking. The environment model needs to be implemented in *changeState()* and *checkAction()* functions in *environment.py* file. A standard goal checking function has been implemented as *checkGoal()* function in the same file. The planner should be implemented in the *getPlan()* function in *planner.py* file.

The default goal in the given code is to put all fruits in the fridge (and keep the fridge closed).

Hint: You can use different search techniques like BFS, DFS, A*, or Reinforcement learning based approaches or even model it as Constrained Satisfaction Problem


## Setup
To setup the PyBullet (physics engine) environment please run the following (assuming python3):
```
pip install -r requirements.txt
```

## Run
To run a plan with the given API and visualize on the simulator run the following command:
```
python planner.py --world jsons/home_worlds/world_home0.json --goal jsons/home_goals/goal0.json
```

## Grading
Your planner would be tested for different goals and different world scenes. The grading scheme would be as follows:
1. Correct implementation of *changeState()* and *checkAction()* functions for different types of actions. (15 points)
2. *getPlan()* function returns correct plan for goal0 - Put apple on table. (10 points)
3. *getPlan()* function returns correct plan for goal1 - Put fruits: apple, orange and banana in box. (10 points)
4. *getPlan()* function returns correct plan for goal2 - Put apple in fridge. (10 points)
5. *getPlan()* function returns correct plan for goal3 - Put fruits in fridge and keep fridge closed. (15 points)
6. *getPlan()* function takes less than half the deadline time (60 seconds) for each goal mentioned above. (10 points)
7. *getPlan()* function returns correct plan for goal3 on other worlds 1 and 2 as well. (15 points)
7. TBA. (15 points)

Note: The grading policy is subject to change without notice.

## Developer
[Shreshth Tuli](www.github.com/shreshthtuli)
