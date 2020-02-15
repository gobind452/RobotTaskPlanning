from environment import *

def getPlan():
	return [["moveTo", "fridge"], \
			   ["changeWing", "up"], \
			   ["changeState", "fridge", "open"], \
			   ["moveTo", "apple"], \
			   ["pick", "apple"], \
			   ["moveTo", "fridge"], \
			   ["dropTo", "fridge"], \
			   ["moveTo", "orange"], \
			   ["pick", "orange"], \
			   ["moveTo", "fridge"], \
			   ["dropTo", "fridge"], \
			   ["moveTo", "banana"], \
			   ["pick", "banana"], \
			   ["moveTo", "fridge"], \
			   ["dropTo", "fridge"], \
			   ["changeState", "fridge", "close"], \
			   ]

# Execute function takes in a plan as input and returns if goal constraints 
# are valid and the final state after plan execution
res, state = execute(getPlan())

print(res)
print(state)