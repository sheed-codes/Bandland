import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# 1. Load data (update path if needed)
df = pd.read_csv("NBA 2024-2025 season - sportsref_(1).csv")

# 2. Clean: drop the first NaN row
df = df.dropna(subset=["Team"]).copy()

# 3. Basic look
print(df.head())
print(df.describe()[["Wins", "3P%", "3P", "3Pt Attempt", "Margin of Victory"]])

# 4. Correlation matrix
corr_cols = ["Wins", "3P%", "3P", "3Pt Attempt",
             "3Pt Attempt Rate", "Margin of Victory",
             "Pythagorean win", "Pythagorean Loss"]
corr = df[corr_cols].corr()
print("\nCorrelation matrix:\n", corr)

# 4a. Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Correlation Heatmap: NBA 2024–25 Team Stats")
plt.tight_layout()
plt.show()

# 5. Simple regression: Wins ~ 3P%
y = df["Wins"]
X = df["3P%"]
X_const = sm.add_constant(X)

model = sm.OLS(y, X_const).fit()
print(model.summary())

# 6. Scatterplot with regression line
plt.figure(figsize=(7, 5))
plt.scatter(df["3P%"], df["Wins"])
plt.xlabel("Team 3-Point Percentage (3P%)")
plt.ylabel("Wins")
plt.title("NBA 2024–25: Wins vs 3P%")

# regression line
x_vals = np.linspace(df["3P%"].min(), df["3P%"].max(), 100)
y_hat = model.params["const"] + model.params["3P%"] * x_vals
plt.plot(x_vals, y_hat)
plt.tight_layout()
plt.show()
