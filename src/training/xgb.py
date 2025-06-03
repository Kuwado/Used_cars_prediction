import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt
import os

def xgboost_training():
    # Đọc dữ liệu
    df = pd.read_csv("../../data/preprocessing/cleaned.csv")

    # One-hot encoding các cột phân loại
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

    # Tách X và y
    X = df_encoded.drop("price", axis=1)
    y = df_encoded["price"]

    # Chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Khởi tạo và train mô hình XGBoost
    print("--------------XGBoost (split)------------------")
    xgb_model = XGBRegressor(
        n_estimators=1000, learning_rate=0.1, max_depth=6, random_state=42, n_jobs=-1
    )
    xgb_model.fit(X_train, y_train)

    model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
    os.makedirs(model_dir, exist_ok=True)
    # Lưu model
    # joblib.dump(xgb_model, "../models/xgboost_model.pkl")
    joblib.dump(xgb_model, os.path.join(model_dir, "xgboost_model.pkl"))

    # Dự đoán
    y_pred = xgb_model.predict(X_test)

    def Accuracy_Score(orig, pred):
        mape = np.mean(100 * np.abs(orig - pred) / orig)
        return 100 - mape

    # Đánh giá
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    accuracy = Accuracy_Score(y_test, y_pred)

    print(f"MAE of XGBoost: {mae:.4f}")
    print(f"RMSE of XGBoost: {rmse:.4f}")
    print(f"R2 of XGBoost: {r2:.4f}")
    print(f"Accuracy (100 - MAPE): {accuracy:.2f}%")

    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values[:100], label="Giá thực tế", marker="o")
    plt.plot(y_pred[:100], label="Giá dự đoán", marker="x")
    plt.title("So sánh giá thực tế và giá dự đoán XGBoost split")
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
    plt.title("So sánh giá thực tế vs giá dự đoán XGBoost split")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Tạo bảng so sánh chỉ gồm Actual Price và Predicted Price
    comparison_df = pd.DataFrame({
        "Actual Price": y_test.values,
        "Predicted Price": y_pred
    })

    # In ra 5 dòng đầu
    print(comparison_df.head())
    
    return {
        "model": "XGBoost",
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "accuracy": accuracy,
    }

xgboost_training()