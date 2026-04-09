import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("dataset.csv")

# -----------------------------
# TRAIN MODEL
# -----------------------------
X = df.drop("book", axis=1)
y = df["book"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

feature_columns = X.columns

# -----------------------------
# FUNCTION: FIND BEST PRICE
# -----------------------------
def find_best_price(user):
    prices = range(5000, 30000, 2000)

    best_price = 0
    max_revenue = 0

    MIN_PROB_THRESHOLD = 0.3

    for price in prices:
        temp = user.copy()
        temp["price"] = price

        temp_df = pd.DataFrame([temp])[feature_columns]

        prob = model.predict_proba(temp_df)[0][1]
        revenue = prob * price

        if prob >= MIN_PROB_THRESHOLD:
            if revenue > max_revenue:
                max_revenue = revenue
                best_price = price

    return best_price, max_revenue


# -----------------------------
# A/B TEST SETUP
# -----------------------------
baseline_revenue = 0
optimized_revenue = 0

segment_results = []

for i in range(len(df)):
    user_full = df.iloc[i]
    
    # Strategy A (Baseline)
    baseline_revenue += user_full["price"] * user_full["book"]

    # Strategy B (Dynamic)
    user = user_full[feature_columns].to_dict()
    best_price, revenue = find_best_price(user)
    optimized_revenue += revenue

    # Store segment data
    segment_results.append({
        "budget": user["budget"],
        "group_size": user["group_size"],
        "optimized_revenue": revenue
    })


# -----------------------------
# RESULTS
# -----------------------------
print("\n--- A/B TEST RESULTS ---")
print("Baseline Revenue (Static Pricing):", baseline_revenue)
print("Optimized Revenue (Dynamic Pricing):", optimized_revenue)

improvement = ((optimized_revenue - baseline_revenue) / baseline_revenue) * 100
print("Revenue Improvement (%):", improvement)


# -----------------------------
# SEGMENT ANALYSIS
# -----------------------------
segment_df = pd.DataFrame(segment_results)

print("\nRevenue by Budget:")
print(segment_df.groupby("budget")["optimized_revenue"].sum())

print("\nRevenue by Group Size:")
print(segment_df.groupby("group_size")["optimized_revenue"].sum())