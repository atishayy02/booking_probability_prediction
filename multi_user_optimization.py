import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("dataset.csv")

# Train model
X = df.drop("book", axis=1)
y = df["book"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Define feature columns
feature_columns = X.columns

# ---- FUNCTION ----
def find_best_price(user):
    prices = range(5000, 30000, 2000)

    best_price = 0
    max_revenue = 0

    for price in prices:
        temp = user.copy()
        temp["price"] = price

        # Ensure correct feature order
        temp_df = pd.DataFrame([temp])[feature_columns]

        prob = model.predict_proba(temp_df)[0][1]
        revenue = prob * price

        if revenue > max_revenue:
            max_revenue = revenue
            best_price = price

    return best_price, max_revenue


# ---- BASELINE ----
baseline_revenue = sum(df["price"] * df["book"])
print("Baseline Revenue:", baseline_revenue)

# ---- OPTIMIZATION ----
total_revenue = 0

for i in range(len(df)):
    user = df.iloc[i][feature_columns].to_dict()
    
    best_price, revenue = find_best_price(user)
    total_revenue += revenue

print("Optimized Revenue:", total_revenue)

# ---- IMPROVEMENT ----
improvement = ((total_revenue - baseline_revenue) / baseline_revenue) * 100
print("Revenue Improvement (%):", improvement)