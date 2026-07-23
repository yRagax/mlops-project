import joblib
from datetime import datetime
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Fetch the dataset
california = fetch_california_housing(as_frame=True)
df = california.frame

# 2. Define Features (X) and Target (y)
X = df.drop(columns="MedHouseVal")
y = df["MedHouseVal"]

# 3. Split the data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Initialize and train the Random Forest Regressor
rf_model = RandomForestRegressor(
    n_estimators=100, random_state=42, max_depth=15, min_samples_leaf=5, n_jobs=-1
)
rf_model.fit(X_train, y_train)

# 5. Make predictions
predictions = rf_model.predict(X_test)

# 6. Evaluate the model
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Mean Squared Error: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

# 7. Save the model
model_name = "rf_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".pkl"
joblib.dump(rf_model, "models/" + model_name, compress=("lzma", 3))
