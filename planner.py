from environment import *
from src.parser import *
from husky_ur5 import execute
import gc

args = initParser()
plannerType = "forward"

class ForwardPlanner(object):
	def __init__(self,env):
		self.env = env
		self.buildHeuristicTree()

	def buildHeuristicTree(self):
		self.parents = dict() # Mapping from objects to parents
		for predicate in self.env.goal:
			if predicate[-1] == "is":
				continue
			if predicate[0] not in self.parents.keys():
				self.parents[predicate[0]] = set()
			if predicate[1] not in self.parents.keys():
				self.parents[predicate[1]] = set()
			self.parents[predicate[0]].add(predicate[1])
		stop = False
		for i in range(len(self.parents.keys())):
			stop = True
			for obj in self.parents.keys():
				if len(self.parents[obj]) <= 1:
					continue
				stop = False
				parent = ""
				if "tray" in self.parents[obj] and "tray2" in self.parents[obj]: # Tray, tray2 and box are the only objects that can be intermediate
					if "tray" in self.parents["tray2"]:
						parent = "tray2"
					else:
						parent = "tray"
				elif "tray" in self.parents[obj]:
					parent = "tray"
				elif "tray2" in self.parents[obj]:
					parent = "tray2"
				elif "box" in self.parents[obj]:
					parent = "box"
				if parent != "":
					self.parents[parent] = self.parents[parent].union(self.parents[obj])
					self.parents[parent].discard(parent)
					self.parents[obj] = set([parent])
			if stop == True:
				break
		for obj in self.parents.keys():
			if len(self.parents[obj]) == 0:
				self.parents[obj] = ""
			else:
				self.parents[obj] = list(self.parents[obj])[0]
		self.depths = dict([(e,0) for e in self.parents.keys()])
		stack = []
		visited = set()
		for obj in self.parents.keys():
			if obj in visited:
				continue
			visited.add(obj)
			stack.append(obj)
			while self.parents[stack[-1]] != "":
				if self.parents[stack[-1]] in visited:
					stack.append(self.parents[stack[-1]])
					break
				visited.add(self.parents[stack[-1]])
				stack.append(self.parents[stack[-1]])
			for i,obj1 in enumerate(reversed(stack)):
				self.depths[obj1] = i + self.depths[stack[-1]]
			stack = []
		self.depth = 0
		for obj in self.parents.keys():
			if self.parents[obj] != "":
				self.depth = self.depth + 1
		self.depth = self.depth +1

	def sortByHeuristic(self,actions):
		score = dict()
		for action in actions:
			score[action] = [0,self.depths[action[1]]] # Emphasize leaf nodes and parent-child
			temp = action[1]
			while temp !="":
				if temp == action[2]:
					score[action][0] = self.depths[action[2]]-self.depths[action[1]]
					break
				temp = self.parents[temp]
			if temp == "":
				score[action][0] = -10
		actions = list(actions)
		actions.sort(key=lambda x:tuple(score[x]))
		return actions

	def searchForPlan(self):
		state = self.env.currState
		stack = [] # DFS Stack
		actionsTaken = [] # Action stack
		actionsSorting = [] # Actions Sort
		if env.checkGoal(state,ignore=False) == True:
			return []
		if 'fridge' in self.env.relevantObjects and state['fridge'] == "close":
			actionsTaken.extend([["moveTo","fridge"],["changeState","fridge","open"]])
		if 'cupboard' in self.env.relevantObjects and state['cupboard'] == "close":
			actionsTaken.extend([["moveTo","cupboard"],["changeState","cupboard","open"]])
		for predicate in self.env.goal:
			if predicate[-1] == "on":
				if (predicate[0] == "tray" and predicate[1] == "tray2") or (predicate[0] == "tray2" and predicate[1] == "tray"):
					if predicate[1] in state['on'][predicate[0]]:
						if predicate[0] not in state['on']["table"]:
							add = "table"
						elif predicate[0] not in state["on"]["table2"]:
							add = "table2"
						actionsTaken.append(["transfer",predicate[1],add])
						break
		for action in actionsTaken:
			state = self.env.changeState(state,action)
		stack.append(state)
		initLength = len(actionsTaken)
		goalDone = False
		while len(stack)!=0:
			if env.checkGoal(stack[-1],ignore=True) == True:
				goalDone = True
				break
			if len(stack) == self.depth: # Reached search depth
				del stack[-1]
				del actionsTaken[-1]
			if len(stack) > len(actionsSorting): # Add actions sort
				applicableActions = self.env.getApplicableActions(stack[-1],eliminate="aggressive")
				actionsSorting.append(self.sortByHeuristic(applicableActions))
			if len(actionsSorting[-1]) == 0: # All actions taken (this state exhausted)
				del stack[-1]
				del actionsSorting[-1]
				if len(actionsTaken)>initLength:
					del actionsTaken[-1]
			else:
				actionsTaken.append(actionsSorting[-1][-1])
				del actionsSorting[-1][-1]
				stack.append(self.env.changeState(stack[-1],list(actionsTaken[-1])))
		plan = []
		if goalDone == False:
			return []
		for action in actionsTaken:
			if action[0] == "transfer":
				plan.extend([["moveTo",action[1]],["pick",action[1]],["moveTo",action[2]],["drop",action[2]]])
			else:
				plan.append(action)
		for predicate in self.env.goal:
			if predicate[-1] == "is":
				if predicate[1] == "close":
					plan.extend([["moveTo",predicate[0]],["changeState",predicate[0],"close"]])
		return plan

class BackwardPlanner(object):
	def __init__(self,env):
		self.env = env
		self.buildHeuristicTree()

	def buildHeuristicTree(self):
		self.parents = dict() # Mapping from objects to parents
		for predicate in self.env.goal:
			if predicate[-1] == "is":
				continue
			if predicate[0] not in self.parents.keys():
				self.parents[predicate[0]] = set()
			if predicate[1] not in self.parents.keys():
				self.parents[predicate[1]] = set()
			self.parents[predicate[0]].add(predicate[1])
		stop = False
		for i in range(len(self.parents.keys())):
			stop = True
			for obj in self.parents.keys():
				if len(self.parents[obj]) <= 1:
					continue
				stop = False
				parent = ""
				if "tray" in self.parents[obj]: # Tray, tray2 and box are the only objects that can be intermediate
					parent = "tray"
				elif "tray2" in self.parents[obj]:
					parent = "tray2"
				elif "box" in self.parents[obj]:
					parent = "box"
				if parent != "":
					self.parents[parent] = self.parents[parent].union(self.parents[obj])
					self.parents[parent].discard(parent)
					self.parents[obj] = set([parent])
			if stop == True:
				break
		for obj in self.parents.keys():
			if len(self.parents[obj]) == 0:
				self.parents[obj] = ""
			else:
				self.parents[obj] = list(self.parents[obj])[0]
		self.depths = dict([(e,0) for e in self.parents.keys()])
		stack = []
		visited = set()
		for obj in self.parents.keys():
			if obj in visited:
				continue
			visited.add(obj)
			stack.append(obj)
			while self.parents[stack[-1]] != "":
				if self.parents[stack[-1]] in visited:
					stack.append(self.parents[stack[-1]])
					break
				visited.add(self.parents[stack[-1]])
				stack.append(self.parents[stack[-1]])
			for i,obj1 in enumerate(reversed(stack)):
				self.depths[obj1] = i + self.depths[stack[-1]]
			stack = []
		self.depth = 0
		for obj in self.parents.keys():
			if self.parents[obj] != "":
				self.depth = self.depth + 1
		self.depth = self.depth +1
		self.depth = 4*self.depth

	def searchForPlan(self):
		global depth
		goal = self.env.goalRepr;
		stack = [] # DFS Stack
		actionsTaken = [] # Action stack
		actionsSorting = [] # Actions Sort
		goalDone = False
		if env.checkGoalRepr(goal,ignore=False) == True:
			return []
		if goal['fridge'] == "close":
			actionsTaken.extend([("changeState","fridge","close"),("moveTo","fridge")])
		if goal['cupboard'] == "close":
			actionsTaken.extend([("changeState","cupboard","close"),("moveTo","cupboard")])
		for action in actionsTaken:
			goal = self.env.regressBackward(goal,list(action))
		stack.append(goal)
		initLength = len(actionsTaken)
		while len(stack)!=0:
			if env.checkGoalRepr(stack[-1],ignore=True) == True:
				goalDone = True
				break
			if len(stack) == self.depth: # Reached search depth
				del stack[-1]
				del actionsTaken[-1]
			if len(stack) > len(actionsSorting): # Add actions sort
				relevantActions = self.env.getRelevantActions(stack[-1],eliminate=False)
				actionsSorting.append(relevantActions)
			if len(actionsSorting[-1]) == 0: # All actions taken (this state exhausted)
				del stack[-1]
				del actionsSorting[-1]
				if len(actionsTaken)>initLength:
					del actionsTaken[-1]
			else:
				actionsTaken.append(actionsSorting[-1][-1])
				del actionsSorting[-1][-1]
				stack.append(self.env.regressBackward(stack[-1],list(actionsTaken[-1])))
		if goalDone == False:
			return []
		if self.env.currState['fridge'] == "close" and "fridge" in self.env.relevantObjects:
			actionsTaken.extend([("changeState","fridge","open"),("moveTo","fridge")])
		if self.env.currState['cupboard'] == "close" and "cupboard" in self.env.relevantObjects:
			actionsTaken.extend([('changeState',"cupboard","open"),("moveTo","cupboard")])
		actionsTaken.reverse()
		for i,action in enumerate(actionsTaken):
			if action[0] == "dropThis":
				actionsTaken[i] = ("drop",action[2])
			actionsTaken[i] = list(actionsTaken[i])
		return actionsTaken
		
@deadline(120)
def getPlan(planner):
	return planner.searchForPlan()
	
env = Environment(args)
if plannerType == "forward":
	planner = ForwardPlanner(env)
else:
	planner = BackwardPlanner(env)
plan = getPlan(planner)
print(plan)
res, state = execute(plan)
print(res)
print(state)