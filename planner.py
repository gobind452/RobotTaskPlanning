from environment import Environment
from src.parser import *
from husky_ur5 import execute
import gc

args = initParser()

depth = 10

class Planner(object):
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
		global depth
		state = self.env.currState;
		stack = [] # DFS Stack
		actionsTaken = [] # Action stack
		actionsSorting = [] # Actions Sort
		if env.checkGoal(self.env.currState,ignore=False) == True:
			return []
		if 'fridge' in self.env.relevantObjects:
			actionsTaken.extend([["moveTo","fridge"],["changeState","fridge","open"]])
		if 'cupboard' in self.env.relevantObjects:
			actionsTaken.extend([["moveTo","cupboard"],["changeState","cupboard","open"]])
		for action in actionsTaken:
			state = self.env.changeState(state,action)
		stack.append(state)
		initLength = len(actionsTaken)
		goalDone = False
		while len(stack)!=0:
			if env.checkGoal(stack[-1],ignore=True) == True:
				goalDone = True
				break
			if len(stack) == depth: # Reached search depth
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

#@deadline(120)
def getPlan(planner):
	return []
	#return planner.searchForPlan()
	
if args.symbolic == "yes":
	env = Environment(args)
	planner = Planner(env)
	plan = getPlan(planner)
	print(plan)
else:
	env = Environment(args)
	planner = Planner(env)
	plan = getPlan(planner)
	res, state = execute(plan)
	print(res,"Goal satisfied")
	print(state)