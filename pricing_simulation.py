import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Load data
df = pd.read_csv("dataset.csv")

# Train model again (simple reuse)
X = df.drop("book", axis=1)
y = df["book"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# ---- SIMULATION FUNCTION ----

def simulate_user(user_features):
    prices = range(5000, 30000, 2000)
    results = []

    for price in prices:
        temp = user_features.copy()
        temp["price"] = price

        # Convert to dataframe
        temp_df = pd.DataFrame([temp])

        prob = model.predict_proba(temp_df)[0][1]
        revenue = prob * price

        results.append((price, prob, revenue))

    return results

# ---- TEST WITH SAMPLE USER ----

sample_user = {
    "search": 1,
    "view": 1,
    "plan": 1,
    "budget": 1,        # medium
    "group_size": 4,
    "days_to_trip": 10,
    "price": 10000      # placeholder
}

results = simulate_user(sample_user)

print("\nPrice Simulation Results:\n")

best_price = 0
max_revenue = 0

for price, prob, revenue in results:
    print(f"Price: {price}, Prob: {prob:.2f}, Revenue: {revenue:.2f}")
    
    if revenue > max_revenue:
        max_revenue = revenue
        best_price = price

print("\nOptimal Price:", best_price)
print("Max Revenue:", max_revenue)