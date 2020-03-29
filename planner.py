from environment import Environment
from src.parser import *
from husky_ur5 import execute

args = initParser()

depth = 10

class Planner(object):
	def __init__(self,env):
		self.env = env

	def sortByHeuristic(self,state,actions):
		scores = []
		for action in actions:
			state = self.env.changeState(state,action)
			scores.append(sum([self.scoreStateForPredicate(state,predicate) for predicate in self.env.goal]))
		actions = zip(scores,actions)
		actions = [x for _,x in sorted(actions)]
		return actions

	def scoreStateForPredicate(self,state,predicate):
		if predicate[-1] == "is":
			return int(state[predicate[0]].lower() == predicate[1].lower())*10
		elif predicate[-1] == "in":
			return int(predicate[0] in state["inside"][predicate[1]])*10
		elif predicate[-1] == "on":
			return int(predicate[0] in state["on"][predicate[1]])*10

	def searchForPlan(self):
		global depth
		state = self.env.currState;
		stack = [] # DFS Stack
		actionsTaken = [] # Action stack
		actionsSorting = [] # Actions Sort
		stack.append(state)
		while len(stack)!=0:
			#print(actionsTaken)
			if env.checkGoal(stack[-1]) == True:
				return actionsTaken # Return plan
			if len(stack) == depth: # Reached search depth
				del stack[-1]
				del actionsTaken[-1]
			if len(stack) > len(actionsSorting): # Add actions sort
				applicableActions = self.env.getApplicableActions(stack[-1],eliminate=True)
				actionsSorting.append(applicableActions)
			if len(actionsSorting[-1]) == 0: # All actions taken (this state exhausted)
				del stack[-1]
				del actionsSorting[-1]
				if len(actionsTaken)>0:
					del actionsTaken[-1]
			else:
				actionsTaken.append(actionsSorting[-1][-1])
				del actionsSorting[-1][-1]
				stack.append(self.env.changeState(stack[-1],list(actionsTaken[-1])))
		return None

#@deadline(120)
def getPlan(planner):
	return [["moveTo","apple"],["pick","apple"],["moveTo","box"],["drop","box"], ["pushTo","box","fridge"], ["changeState","fridge","open"], ["pick","box"], ["drop","fridge"]]
	return planner.searchForPlan(env)
	
if args.symbolic == "yes":
	env = Environment(args)
	planner = Planner(env)
	plan = getPlan(planner)
	print(plan)
else:
	res, state = execute(getPlan(None))
	print(res)
	print(state)