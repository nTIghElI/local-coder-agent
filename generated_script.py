import random

def roll_dice(num_sides, num_rolls):
    total = sum(random.randint(1, num_sides) for _ in range(num_rolls))
    return total / num_rolls

average = roll_dice(20, 10)
print("Average roll:", average)