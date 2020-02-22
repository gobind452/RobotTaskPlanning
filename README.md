# COL864: Homework II
## Overview
* This exercise concerns writing a symbolic planner for an agent (mobile manipulator) capable of interacting with objects in a virtual environment. The robot can perform a set of actions (move to, pick, place on, push to, open/close) which are described below. 
* We assume a discrete world representation where the environment can be represented as a set of objects. The robot can move towards a given object or peform interactions with it. 
* Some objects in the scene can have symbolic states. For example, a cupboard can be open or closed. We can assume that the robot can determine if an object is open or closed, if an object is inside or on top of an object or if it is close to an object 
of interest. 
* Note that the agent does not know the semantics of when actions are applicable and what are their effects. Hence, cannot perform tasks such as moving an object to a goal location that requires chaining of actions. 
* Your objective is enable the robot with a task planner allowing it to perform tasks that require reasoning over a sequence of objects.  

## Simulation Environment
### Virtual Environment 
* The simulation is based on PyBullet simulator with a mobile manipulator (called Husky robot with a manipulator arm. 
* The simulator consists of 10 world scenes and 5 different goals. A screenshot of the simulator appears below:
<div align="center">
<img src="https://github.com/shreshthtuli/COL864-Task-Planning/blob/master/screenshot.png" width="700" align="middle">
</div>
Note: All actions are symbolic and robot position is discretized by proximity to objects.

To setup the PyBullet (physics engine) environment please run the following (assuming python3):
```
pip install -r requirements.txt
```

### World State 
The world state at any time instant can be accessed as a python dictionary of the form: 
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

### Agent Actions
The robot can preform simple actions like move, pick, drop, open/close doors and push objects. To simulate a plan in the simulation environment you may use the following functions:
* \[moveTo, object\] - moves robot close to object
* \[pick, object\] - picks the specified object
* \[drop, destination\] - drops a grabbed object to destination object
* \[changeState, object, state\] - changes the state of an object (open or close)
* \[pushTo, object, destination\] - pushes object close to the destination object

A  plan is a sequence (python list) of the afore mentioned actions with objects in the set - (apple, orange, banana, table, table2, box, fridge, tray, tray2). You can input a plan to the *execute()* function which outputs a pair (plan success, final state after plan execution).

To run a plan with the given API and visualize on the simulator run the following command:
```
python planner.py --world jsons/home_worlds/world_home0.json --goal jsons/home_goals/goal0.json
```


## Problem Statement
The goal of this exercise is to write a symbolic planner enabling the agent to perform a variety of tasks requiring navigation and interaction actions. 
* Please implement a model of actions in terms of when they are feasible and how actions can change the world state. The environment model needs to be implemented in *changeState()* and *checkAction()* functions in *environment.py* file.
* Implement a planner that can synthesize a feasible plan consisting of a sequence of actions to attain the goal state given the initial state of the world. 
 A standard goal checking function has been implemented as *checkGoal()* function. The planner should be implemented in the *getPlan()* function in *planner.py* file. You may visualize the plan in the simulator with the instructions below. The default goal in the given code is to put all fruits in the fridge (and keep the fridge closed). 
* Formally write down the domain representation and the planning algorithm. Implement implement a forward and a backward planning strategy. Please compare the running time, branching factor and explain the advantages or disadvantages of both. 
* Next, improve the planner to synthesize plans in a short amount of time. For example, return a feasible plan under 60 seconds. You may explore techniques for 
accelerating search ( e.g., via heuristics) building off material in the class and exploring techniques from your reading. There is extra credit for this part of the homework. 

<!-- You are expected to build a planner for robots in diverse environments with complex interactions. You need to develop an approximate environment model which is able to change the state corresponding to an input action with action feasibility checking. The environment model needs to be implemented in *changeState()* and *checkAction()* functions in *environment.py* file. A standard goal checking function has been implemented as *checkGoal()* function in the same file. The planner should be implemented in the *getPlan()* function in *planner.py* file.

The default goal in the given code is to put all fruits in the fridge (and keep the fridge closed).

Hint: You can use different search techniques like BFS, DFS, A*, or Reinforcement learning based approaches or even model it as Constrained Satisfaction Problem
-->

## Evaluation
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
