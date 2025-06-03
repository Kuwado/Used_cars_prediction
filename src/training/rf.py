import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import os

def random_forest_training():
    # Đọc dữ liệu đã one-hot encode
    df = pd.read_csv("../../data/preprocessing/cleaned.csv")

    # One-hot encoding các cột categorical
    df_encoded = pd.get_dummies(
        df,
        columns=[
            "brand",
            "model",
            "fuel_type",
            "transmission",
            "origin",
            "car_type",
        ],
    )

    # joblib.dump(
    #     df_encoded.drop("price", axis=1).columns.tolist(), "../models/model_columns.pkl"
    # )

    model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(
        df_encoded.drop("price", axis=1).columns.tolist(),
        os.path.join(model_dir, "model_columns.pkl")
    )


    # Tách đặc trưng và target
    X = df_encoded.drop("price", axis=1)
    y = df_encoded["price"]

    # Chia dữ liệu train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Khởi tạo và train Random Forest
    print("--------------Random Forest (split)------------------")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
   
    # Lưu model
    # joblib.dump(rf_model, "../models/random_forest_model.pkl")
    joblib.dump(rf_model, os.path.join(model_dir, "random_forest_model.pkl"))

    # Dự đoán
    y_pred = rf_model.predict(X_test)

    def Accuracy_Score(orig, pred):
        mape = np.mean(100 * np.abs(orig - pred) / orig)
        return 100 - mape

    # Đánh giá model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    accuracy = Accuracy_Score(y_test, y_pred)

    print(f"MAE of Random Forest: {mae:.4f}")
    print(f"RMSE of Random Forest: {rmse:.4f}")
    print(f"R2 of Random Forest: {r2:.4f}")
    print(f"Accuracy (100 - MAPE): {accuracy:.2f}%")

    # Tạo bảng so sánh giá thực tế và giá dự đoán
    comparison_df = pd.DataFrame({
        "Actual Price": y_test.values,
        "Predicted Price": y_pred
    })
    print(comparison_df.head())

    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values[:100], label="Giá thực tế", marker='o')
    plt.plot(y_pred[:100], label="Giá dự đoán", marker='x')
    plt.title("So sánh giá thực tế và giá dự đoán Random Forest split")
    plt.xlabel("Mẫu")
    plt.ylabel("Giá xe")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, edgecolors="k")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Giá thực tế")
    plt.ylabel("Giá dự đoán")
    plt.title("So sánh giá thực tế vs giá dự đoán Random Forest split")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return {
        "model": "Random Forest",
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "accuracy": accuracy,
    }

random_forest_training()