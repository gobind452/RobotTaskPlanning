## Overview
* This exercise concerns writing a symbolic planner for an agent (mobile manipulator) capable of interacting with objects in a virtual environment. 
* The robot in the virtual environment is capable of performing a set of actions (move to, pick, place on, push to, open/close) which are described below. 
* The robot's environment can be represented as a set of objects. The robot can move towards a given object or peform interactions with it. 
* Some objects in the scene can have symbolic states. For example, a cupboard can be open or closed. Assume that the robot can determine if an object is open or closed, if an object is inside or on top of an object or if it is close to an object 
of interest. 
* The agent *does not know* the semantics of when actions are applicable and what are their effects. Hence, cannot perform tasks such as moving an object to a goal location that requires reasoning about a sequence of actions to accomplish a goal. 
* Your objective is endow the robot with a task planner enabling it to perform semantic tasks in the environment.   

## Simulation Environment
### Virtual Environment 
* The simulation environment is based on PyBullet physics simulator with a mobile manipulator (a robot called Husky with a manipulator arm. 
* The simulator consists of 10 world scenes and 5 different goals. A screenshot of the simulator appears below:
<div align="center">
<img src="https://github.com/shreshthtuli/COL864-Task-Planning/blob/master/screenshot.png" width="700" align="middle">
</div>
Note: All actions are symbolic and robot position is discretized by proximity to objects.

To setup the PyBullet (physics engine) environment please run the following (assuming python3):
```
pip install -r requirements.txt
```

A sample task execution on this simulator can be seen [here](https://youtu.be/-mIQuM3kjF4)

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

The initial state of the simulator can be initialized with different world scenes encoded in JSON format in directory *jsons/home_worlds/*. You can create new world scenes for testing.

### Agent Actions
The robot can preform the following actions: move, pick, drop, open/close doors and push objects. To simulate a plan in the simulation environment you can use the following functions:
* \[moveTo, object\] - moves robot close to object
* \[pick, object\] - picks the specified object
* \[drop, destination\] - drops a grabbed object to destination object
* \[changeState, object, state\] - changes the state of an object (open or close)
* \[pushTo, object, destination\] - pushes object close to the destination object

A  symbolic plan consists of a sequence (a python list) of the afore mentioned actions parameterized with the objects in the set - (apple, orange, banana, table, table2, box, fridge, tray, tray2). You can input a plan to the *execute()* function which outputs a pair (plan success, final state after plan execution).

To run a plan with the given API and visualize on the simulator run the following command:
```
python planner.py --world jsons/home_worlds/world_home0.json --goal jsons/home_goals/goal0.json
```
Note: If you have a system that does not have a dedicated GPU or want to run on server or HPC with no graphics capabilities, you can add the option *--display tp* to the above command. This will save a sequence of third person perspective images in the logs folder.

## Sample state,action sequence

* t0 : {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': []}
* action = \[moveTo, apple\] 
* t1 = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': \['apple'\]}
* action = \[pick, apple\]
* t2 = {'grabbed': 'apple', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [], 'close': \['apple'\]}

## Environment.py

The environment.py models all the state action transitions which are permitted in this simulation. It also contains function for getting applicable actions (i.e actions that can be taken at a particular state) and relevant actions (i.e actions that could have been take to reach a particular state) as a function of the state. The applicable actions are used for forward planning, and the relevant actions are used for the backward planning from the goal. 

## Planner.py

The planner.py contains two classes : ForwardPlanner and BackwardPlanner. Given a set of predicates which are true in the initial state, and a set of predicates which define a goal, the planners find a sequence of actions which could help reach the robot the goal from the initial state. It also uses various heuristics to prune the search space for plans. 

## Developer
This exercise is based on the simulation tool developed as part of an undergraduate project at Dept. of CSE, IITD led by 
[Shreshth Tuli](www.github.com/shreshthtuli). This exercise was given as a part of the course Learning for Robotics (COL864) at IITD under Prof Rohan Paul.
<br>
The solution (planner.py and environment.py) was implemented by [Gobind Singh](www.github.com/gobind452)
