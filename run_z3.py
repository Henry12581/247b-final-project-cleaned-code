from z3 import *
# Define variables
mike_share = Int('mike_share')
johnson_share = Int('johnson_share')

# Set up the ratio and Johnson's share
s = Solver()
s.add(mike_share * 5 == johnson_share * 2)  # 2:5 ratio (Mike:Johnson)
s.add(johnson_share == 2500)

# Solve for Mike's original share
s.check()
model = s.model()
mike_original = model[mike_share].as_long()

# Calculate Mike's remaining amount after spending $200
mike_remaining = mike_original - 200
print(mike_remaining)