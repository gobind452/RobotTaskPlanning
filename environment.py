from copy import deepcopy
import husky_ur5
import symbolic_utils
import json
from src.parser import *

state = husky_ur5.getCurrentState() # Get initial states
args = initParser()
print(state)

if args.symbolic == "yes":
	husky_ur5.destroy() # Destroy the GUI for now

objects = set(['apple', 'orange', 'banana', 'table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard'])
enclosures = set(['fridge', 'cupboard']) # Can be open or closed
canContain = set(['fridge','cupboard','box']) # Can contain objects (In predicate)
canSupport = set(['table','table2','tray','tray2']) # Can support objects (On predicate)
actionTemplates = ['moveTo', 'pick', 'drop', 'changeState', 'pushTo','transfer'] 
canPlaced = set(['apple','orange','banana','tray','tray2','box']) # Can be placed in or on
cantPick = set(['fridge','cupboard','table','table2']) # Cant pick these objects
constraints = set([('box','tray'),('box','tray2')])

actionGroundings = set()
goalBasedActionGroundings = set()
transferActionGroundings = set()

class Environment(object):
	def __init__(self,args):
		global state
		self.world = args.world
		self.goal = []
		self.loadGoal(args.goal)
		self.currState = {'grabbed':state['grabbed'],'fridge':state['fridge'].lower(),'cupboard':state['cupboard'].lower(),'close':set(state['close'])}
		self.currState['inside'] = dict([(e,set()) for e in canContain])
		self.currState['on'] = dict([(e,set()) for e in canSupport])
		for rel in state['inside']:
			self.currState['inside'][rel[1]].add(rel[0])
		for rel in state['on']:
			self.currState['on'][rel[1]].add(rel[0])
		self.buildActionGroundings()

	def loadGoal(self,goal):
		with open(goal) as json_file:
			goalDescription = json.load(json_file)['goals']
		for goal in goalDescription:
			obj,target,state = goal['object'],goal['target'],goal['state']
			if state != "":
				self.goal.append((obj,state,"is"))
				continue
			if target in canContain:
				self.goal.append((obj,target,"in"))
			if target in canSupport:
				self.goal.append((obj,target,"on"))

	def checkAction(self,state, action):
		if action[0] == "pick":
			if action[1] not in state['close']:
				return False # First get close to the object
			if action[1] in cantPick:
				return False # Cant pick this object
			if action[1] == state['grabbed']:
				return False # Already picked
		
		elif action[0] == "drop":
			if state['grabbed'] == "":
				return False # Grab objects first
			if action[1] not in state['close']: # Destination not close, move there first
				return False
			if action[1] == state['grabbed']: # Cant drop object on itself
				return False
			if action[1] not in canContain and action[1] not in canSupport: # Cant drop object here
				return False
			if action[1] in enclosures:
				if state[action[1]].lower() == "close":
					return False # First open enclosure
			if (state['grabbed'],action[1]) in constraints:
				return False
		
		elif action[0] == "changeState":
			if state['grabbed']!= "":
				return False # Robot hand not free
			if action[1] not in enclosures:
				return False
			if action[2].lower() == state[action[1]].lower():
				return False # Already done
			if action[1] not in state['close']:
				return False
		
		elif action[0] == "pushTo":
			if action[1] not in state['close']: # Object not close
				return False
			if state['grabbed']!="":
				return False # Already have a object
			if action[1] == action[2]:
				return False # Destination is start
			if action[1] in cantPick: # Cant pick this object
				return False
		
		elif action[0] == "transfer":
			if action[2] not in canContain and action[2] not in canSupport:
				return False
			if (action[1],action[2]) in constraints:
				return False
			if action[1] not in canPlaced:
				return False
			if state["grabbed"] != "":
				return False
			if action[2] in enclosures and state[action[2]].lower() == "close":
				return False
			if action[1] == action[2]:
				return False
			if action[2] in canSupport:
				if action[1] in state['on'][action[2]]:
					return False
			elif action[2] in canContain:
				if action[1] in state['inside'][action[2]]:
					return False

		return True

	def changeState(self,state1, action): # Assumes action is possible
		state = deepcopy(state1)

		if action[0] == "moveTo":
			state['close'] = []
			if state['grabbed'] != "": # Grabbed object remains close
				state['close'].append(state['grabbed'])
			state['close'].append(action[1])
			for obj in state['close']:
				if obj in canContain:
					state['close'].extend(list(state['inside'][obj])) # Add all obj inside that object
				if obj in canSupport:
					state['close'].extend(list(state['on'][obj])) # Add all obj on that object
			state['close'] = set(state['close'])

		elif action[0] == "pick": 
			state['grabbed'] = action[1] # Make that object grabbed
			for obj in canContain:
				state['inside'][obj].discard(action[1]) # Remove that object out of a box
			for obj in canSupport:
				state['on'][obj].discard(action[1]) # Remove that object where it is placed
			if action[1] in canContain:
				for obj in state['inside'][action[1]]: # Objects inside the picked object
					for obj2 in canContain:  # We want to remove the constraints
						if obj2 == action[1] or obj2 in state['inside'][action[1]]: # The internal hierarchy of objects is not changed
							continue
						state['inside'][obj2].discard(obj) # All objects in the pick object are not now in their original parent above it
			if action[1] in canSupport:
				for obj in state['on'][action[1]]: # Objects inside the picked object
					for obj2 in canSupport:  # We want to remove the constraints
						if obj2 == action[1] or obj2 in state['on'][action[1]]: # The internal hierarchy of objects is not changed
							continue
						state['on'][obj2].discard(obj) # All objects in the pick object are not now in their original parent above it
			
		elif action[0] == "drop":
			if action[1] in canContain:
				state['inside'][action[1]].add(state['grabbed']) # Add obj inside
				if state['grabbed'] in canContain:
					for obj in state['inside'][state['grabbed']]:
						state['inside'][action[1]].add(obj)
				elif state['grabbed'] in canSupport:
					for obj in state['on'][state['grabbed']]:
						state['inside'][action[1]].add(obj)
			elif action[1] in canSupport:
				state['on'][action[1]].add(state['grabbed']) # Add obj on
				if state['grabbed'] in canContain:
					for obj in state['inside'][state['grabbed']]:
						state['on'][action[1]].add(obj)
				if state['grabbed'] in canSupport:
					for obj in state['on'][state['grabbed']]:
						state['on'][action[1]].add(obj)
			state['grabbed'] = ""

		elif action[0] == "changeState":
			state[action[1]] = action[2].lower() # Change state
		
		elif action[0] == "pushTo": # Push object from source to destination
			state = self.changeState(state,["pick",action[1]]) # Grab object
			state = self.changeState(state,["moveTo",action[2]]) # Move to destination
			state['grabbed'] = "" # Leave object here

		elif action[0] == "transfer":
			state = self.changeState(state,["moveTo",action[1]])
			state = self.changeState(state,["pick",action[1]])
			state = self.changeState(state,["moveTo",action[2]])
			state = self.changeState(state,["drop",action[2]])

		return state

	def buildActionGroundings(self):
		global actionGroundings
		for obj in objects:
			actionGroundings.add(("moveTo",obj))
		for obj in objects-cantPick:
			actionGroundings.add(("pick",obj))
		for obj in canSupport:
			actionGroundings.add(("drop",obj))
		for obj in canContain:
			actionGroundings.add(("drop",obj))
		for obj in enclosures:
			actionGroundings.add(("changeState",obj,"open"))
			actionGroundings.add(("changeState",obj,"close"))
		for obj in objects-cantPick:
			for obj1 in objects:
				if obj == obj1:
					continue
				actionGroundings.add(("pushTo",obj,obj1))
		global goalBasedActionGroundings
		self.relevantObjects = set()
		for predicate in self.goal:
			if predicate[-1] == "is":
				self.relevantObjects.add(predicate[0].lower())
			else:
				self.relevantObjects.add(predicate[0])
				self.relevantObjects.add(predicate[1])
		firstOrderRelevantObjects = set()
		for obj in canContain:
			for obj1 in self.currState['inside'][obj]:
				if obj1 in self.relevantObjects:
					firstOrderRelevantObjects.add(obj)
		for obj in canSupport:
			for obj1 in self.currState['on'][obj]:
				if obj1 in self.relevantObjects:
					firstOrderRelevantObjects.add(obj)
		self.relevantObjects = self.relevantObjects.union(firstOrderRelevantObjects)
		for obj in self.relevantObjects:
			goalBasedActionGroundings.add(("moveTo",obj))
		for obj in self.relevantObjects-cantPick:
			goalBasedActionGroundings.add(("pick",obj))
		for obj in self.relevantObjects.intersection(canSupport):
			goalBasedActionGroundings.add(("drop",obj))
		for obj in self.relevantObjects.intersection(canContain):
			goalBasedActionGroundings.add(("drop",obj))
		for obj in self.relevantObjects.intersection(enclosures):
			goalBasedActionGroundings.add(("changeState",obj,"open"))
			goalBasedActionGroundings.add(("changeState",obj,"close"))
		for obj in self.relevantObjects-cantPick:
			for obj1 in self.relevantObjects:
				if obj == obj1 :
					continue
				goalBasedActionGroundings.add(("pushTo",obj,obj1))
		for obj in self.relevantObjects-firstOrderRelevantObjects:
			for obj1 in self.relevantObjects-firstOrderRelevantObjects:
				if obj == obj1:
					continue
				transferActionGroundings.add(("transfer",obj,obj1))
		del firstOrderRelevantObjects


	def getApplicableActions(self,state,eliminate=False):
		applicableActions = list()
		if eliminate == False:
			for action in actionGroundings:
				if self.checkAction(state,list(action)) == True:
					applicableActions.append(action)
		elif eliminate == True: # Goal based elimination of actions
			for action in goalBasedActionGroundings:
				if self.checkAction(state,list(action)) == True:
					applicableActions.append(action)
		elif eliminate == "aggressive": # Only the transfer action
			for action in transferActionGroundings:
				if self.checkAction(state,list(action)) == True:
					applicableActions.append(action)
		return applicableActions
		
	def checkGoal(self,state,ignore=False):
		for predicate in self.goal:
			if predicate[-1] == "is" and ignore == True:
				continue
			check = self.checkPredicate(state,predicate)
			if check == False:
				return False
		return True

	def checkPredicate(self,state,predicate):
		if predicate[-1] == "is":
			return state[predicate[0]].lower() == predicate[1].lower()
		if predicate[-1] == "in":
			return predicate[0] in state["inside"][predicate[1]]
		else:
			return predicate[0] in state["on"][predicate[1]]

	def canBePlaced(self,obj1,obj2):
		if obj1 not in canPlaced:
			return False
		if obj2 not in canSupport and obj2 not in canContain:
			return False
		if (obj1,obj2) in constraints:
			return False
		return True