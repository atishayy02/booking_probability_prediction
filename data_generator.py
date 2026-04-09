import pandas as pd
import random

data = []

for i in range(1000):
    # User journey
    search = 1
    view = 1 if random.random() > 0.1 else 0
    plan = 1 if view == 1 and random.random() > 0.2 else 0

    # User features
    budget = random.choice([0, 1, 2])  # 0=Low, 1=Medium, 2=High
    group_size = random.choice([2, 3, 4, 5])
    days_to_trip = random.randint(1, 30)

    # Price
    price = random.randint(5000, 30000)

    # ---- REALISTIC BOOKING LOGIC ----
    prob = 0.6

    # Lower probability if high price
    prob -= (price / 60000)

    # Increase if user planned
    if plan == 1:
        prob += 0.2

    # Budget effect
    if budget == 1:  # Medium
        prob += 0.1
    elif budget == 0:  # Low
        prob -= 0.1

    # Group effect
    if group_size >= 4:
        prob += 0.05

    # Clamp probability between 0 and 1
    prob = max(0, min(prob, 1))

    # Final booking decision
    book = 1 if random.random() < prob else 0

    data.append([
        search, view, plan,
        budget, group_size,
        days_to_trip, price,
        book
    ])

df = pd.DataFrame(data, columns=[
    "search", "view", "plan",
    "budget", "group_size",
    "days_to_trip", "price",
    "book"
])

df.to_csv("dataset.csv", index=False)

print("Dataset created!")