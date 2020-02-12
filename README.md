# COL864-Task-Planning
Assignment for the COL864 - Special topics in AI (Robotics) course at IITD.
Objective: Gaining exposure to a virtual environment with a simulated robot agent that can interact with objects in the scene. Formulating and solving a symbolic planning problem. 

## API
To execute a plan in the simulation environment you can use the following functions:
* \[moveTo, object\] - moves robot close to object
* \[changeWing, state\] - changes the robot gripper to specified state (up or home)
* \[pick, object\] - picks the specified object
* \[drop, destination\] - drops a grabbed object to destination object
* \[changeState, object, state\] - changes the state of an object (open or close)
* \[pushTo, object, destination\] - pushes object close to the desitnation object
A  plan is a list of the above mentioned functions with objects in the set - (apple, orange, banana, table, table2, box, cupboard, tray)


## Setup
To setup the PyBullet (physics engine) environment please run the following:
```
pip install -r requirements.txt
```

## Run
To run a plan with the given API and visualize on the simulator run the following command:
```
python planner.py --world jsons/home_worlds/world_home0.json
```
