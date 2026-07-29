import os
import dotenv
import mlflow
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load environmental variables
dotenv.load_dotenv()
MLFLOW_URI = str(os.getenv("MLFLOW_URI"))

# Initialize MLflow
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment("California Housing Price Prediction")

# Fetch the dataset
california = fetch_california_housing(as_frame=True)
df = california.frame

# Split the data (80% training, 20% testing)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
train_dataset = mlflow.data.from_pandas(
    df_train, name="california_housing", targets="MedHouseVal"
)
test_dataset = mlflow.data.from_pandas(
    df_test, name="california_housing", targets="MedHouseVal"
)

# Define Features (X) and Target (y)
X_train = df_train.drop(columns="MedHouseVal")
X_test = df_test.drop(columns="MedHouseVal")
y_train = df_train["MedHouseVal"]
y_test = df_test["MedHouseVal"]

for n_estimators in [50, 100, 500]:
    for max_depth in [5, 10, 15]:
        for min_samples_leaf in [2, 5, 10]:
            # 4. Initialize and train the Random Forest Regressor
            rf_model = RandomForestRegressor(
                n_estimators=n_estimators,
                random_state=42,
                max_depth=max_depth,
                min_samples_leaf=min_samples_leaf,
                n_jobs=-1,
            )
            rf_model.fit(X_train, y_train)

            # Make predictions
            predictions = rf_model.predict(X_test)

            # Evaluate the model
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            # Log parameters, metrics, and model to MLflow
            with mlflow.start_run() as run:
                mlflow.log_input(train_dataset, context="train")
                mlflow.log_input(test_dataset, context="test")
                mlflow.log_param("n_estimators", n_estimators)
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("min_samples_leaf", min_samples_leaf)
                mlflow.log_metric("mse", mse)
                mlflow.log_metric("r2", r2)
                mlflow.sklearn.log_model(
                    rf_model,
                    name=f"model_{n_estimators}_{max_depth}_{min_samples_leaf}",
                    input_example=X_test.iloc[:5],
                )
