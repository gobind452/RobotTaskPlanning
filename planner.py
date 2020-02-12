from husky_ur5 import *

res = execute([["moveTo", "cupboard"], \
			   ["changeWing", "up"], \
			   ["changeState", "cupboard", "open"], \
			   ["moveTo", "cube_red"], \
			   ["pick", "cube_red"], \
			   ["moveTo", "cupboard"], \
			   ["dropTo", "cupboard"], \
			   ["moveTo", "cube_green"], \
			   ["pick", "cube_green"], \
			   ["moveTo", "cupboard"], \
			   ["dropTo", "cupboard"], \
			   ["moveTo", "cube_gray"], \
			   ["pick", "cube_gray"], \
			   ["moveTo", "cupboard"], \
			   ["dropTo", "cupboard"], \
			   ])

print(res)