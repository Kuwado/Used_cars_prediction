import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../../../data/preprocessing/preprocessing.csv")


# Xóa các bản ghi có số lượng brand < 10
brand_counts = df["brand"].value_counts()
brands_to_keep = brand_counts[brand_counts >= 10].index
df = df[df["brand"].isin(brands_to_keep)]

model_counts = df["model"].value_counts()
models_to_keep = model_counts[model_counts >= 10].index
df = df[df["model"].isin(models_to_keep)]

car_type_counts = df["car_type"].value_counts()
car_types_to_keep = car_type_counts[car_type_counts >= 10].index
df = df[df["car_type"].isin(car_types_to_keep)]

counts = df["car_type"].value_counts()

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=counts.index, y=counts.values)

# Thêm số lượng vào đầu mỗi cột
for i, value in enumerate(counts.values):
    plt.text(i, value + 2, str(value), ha="center", va="bottom", fontsize=10)

plt.title("Số lượng xe theo Model")
plt.ylabel("Số lượng")
plt.xlabel("Model")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()

for col in df.columns:
    print(f"\n🟦 Cột: {col}")
    print(f"Số lượng giá trị khác nhau: {df[col].nunique()}")
    print("Giá trị và số lượng tương ứng:")
    print(df[col].value_counts())
    print("---------------------------------------------------")

df.to_csv("../../../data/preprocessing/cleaned.csv", index=False)
print(f"Số bản ghi sau khi tiền xử lý: {df.shape[0]}")
