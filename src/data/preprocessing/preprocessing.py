import pandas as pd
import os

# df = pd.read_csv("../../../data/raw/chotot_xe_data.csv")
df = pd.read_csv("../../../data/preprocessing/raw.csv")


# In số dòng và số cột
print(f"Số bản ghi: {df.shape[0]}")
print(f"Số cột: {df.shape[1]}")

# In tên các cột
print("\nTên các cột:")
print(df.columns.tolist())

# Xóa các cột không cần thiết
columns_to_drop = [
    "id",
    "title",
    "location",
    "post_time",
    "crawl_time",
]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# Chuyển cột 'price' xuống cuối
if "price" in df.columns:
    price_col = df["price"]
    df = df.drop(columns=["price"])
    df["price"] = price_col

# In tên các cột
print(f"Số bản ghi: {df.shape[0]}")
print(f"Số cột: {df.shape[1]}")
print(df.columns.tolist())
print("---------------------------------------")
print(df.info())
print("---------------------------------------")
print(df.describe())
print("---------------------------------------")
print("Lượng data bị thiếu\n")
print(df.isnull().sum())

# In số lượng giá trị duy nhất của từng cột
# for col in df.columns:
#     print(f"\n🟦 Cột: {col}")
#     print(f"Số lượng giá trị khác nhau: {df[col].nunique()}")
#     print("Giá trị và số lượng tương ứng:")
#     print(df[col].value_counts())
#     print("---------------------------------------------------")

# Do owner chỉ có 1 giá trị và null nhiều => xóa
df = df.drop(columns=["owners"])
df = df.drop(columns=["condition"])

# xóa bản ghi có null
df = df.dropna()
null_rows_count = df.isna().any(axis=1).sum()

count = df[df["car_type"] == "--"].shape[0]
print(f"Số lượng bản ghi có car_type = '--': {count}")
df = df[df["car_type"] != "--"]

duplicate_count = df.duplicated().sum()
print(f"Số bản ghi trùng lặp: {duplicate_count}")

df_cleaned = df.drop_duplicates()
print(f"Số bản ghi sau khi fill: {df.shape[0]}")
null_rows_count = df.isna().any(axis=1).sum()
print(f"Số dòng có giá trị NULL: {null_rows_count}")
print(f"Số cột: {df.shape[1]}")
print(df.columns.tolist())


df.to_csv("../../../data/preprocessing/preprocessing.csv", index=False)
