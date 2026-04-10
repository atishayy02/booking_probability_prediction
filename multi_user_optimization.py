import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

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
def find_best_price(user, threshold):
    prices = range(5000, 30000, 2000)

    best_price = 0
    max_revenue = 0

    for price in prices:
        temp = user.copy()
        temp["price"] = price

        temp_df = pd.DataFrame([temp])[feature_columns]

        prob = model.predict_proba(temp_df)[0][1]
        revenue = prob * price

        # Apply threshold constraint
        if prob >= threshold:
            if revenue > max_revenue:
                max_revenue = revenue
                best_price = price

    return best_price, max_revenue


# -----------------------------
# BASELINE REVENUE (STATIC PRICING)
# -----------------------------
baseline_revenue = sum(df["price"] * df["book"])

print("\n--- A/B TEST + THRESHOLD ANALYSIS ---")
print("Baseline Revenue (Static Pricing):", baseline_revenue)

# -----------------------------
# THRESHOLD TESTING
# -----------------------------
thresholds = [0.2, 0.3, 0.4]

for threshold in thresholds:
    optimized_revenue = 0
    segment_results = []

    for i in range(len(df)):
        user_full = df.iloc[i]

        # Dynamic Pricing
        user = user_full[feature_columns].to_dict()
        best_price, revenue = find_best_price(user, threshold)
        optimized_revenue += revenue

        # Store segment data
        segment_results.append({
            "budget": user["budget"],
            "group_size": user["group_size"],
            "optimized_revenue": revenue
        })

    improvement = ((optimized_revenue - baseline_revenue) / baseline_revenue) * 100

    print(f"\n--- Threshold: {threshold} ---")
    print("Optimized Revenue:", optimized_revenue)
    print("Revenue Improvement (%):", improvement)

    # -----------------------------
    # SEGMENT ANALYSIS
    # -----------------------------
    segment_df = pd.DataFrame(segment_results)

    print("\nRevenue by Budget:")
    print(segment_df.groupby("budget")["optimized_revenue"].sum())

    print("\nRevenue by Group Size:")
    print(segment_df.groupby("group_size")["optimized_revenue"].sum())


 # -----------------------------
# VISUALIZATION (SINGLE USER)


# Pick a sample user
sample_user = df.iloc[0][feature_columns].to_dict()

prices = list(range(5000, 30000, 2000))
probs = []
revenues = []

for price in prices:
    temp = sample_user.copy()
    temp["price"] = price

    temp_df = pd.DataFrame([temp])[feature_columns]

    prob = model.predict_proba(temp_df)[0][1]
    revenue = prob * price

    probs.append(prob)
    revenues.append(revenue)

# Plot Probability vs Price
plt.figure()
plt.plot(prices, probs)
plt.xlabel("Price")
plt.ylabel("Booking Probability")
plt.title("Price vs Booking Probability")
plt.show()

# Plot Revenue vs Price
plt.figure()
plt.plot(prices, revenues)
plt.xlabel("Price")
plt.ylabel("Expected Revenue")
plt.title("Price vs Revenue")
plt.show()