from z3 import *

# Define variables
mike_share = Real('mike_share')
johnson_share = Real('johnson_share')

# Create solver
s = Solver()

# Add ratio constraint: Mike:Johnson = 2:5
s.add(mike_share / 2 == johnson_share / 5)

# Add Johnson's share constraint
s.add(johnson_share == 2500)

# Solve
if s.check() == sat:
    model = s.model()
    mike_total = model[mike_share].as_decimal(2)
    mike_remaining = float(mike_total) - 200

    print(f"Mike's total share: ${mike_total}")
    print(f"Mike's remaining money after buying shirt: ${mike_remaining}")
else:
    print("No solution found")