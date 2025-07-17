import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import os
import re
import tkinter as tk
from tkinter import filedialog

#Select the file path
def get_file_path():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Bring to front
    file_path = filedialog.askopenfilename(title="Select a file")
    root.destroy()
    return file_path
    
path = get_file_path()
print("Selected path:", path)
file_path=path
# 🔹 Check if file exists
if not os.path.exists(file_path):
    print("❌ File not found. Please check the path and try again.")
    exit()

# 🔹 Load file based on extension
if file_path.endswith('.csv'):
    df = pd.read_csv(file_path)
elif file_path.endswith(('.xlsx', '.xls')):
    df = pd.read_excel(file_path)
else:
    print("❌ Unsupported file type. Please provide a .csv or .xlsx file.")
    exit()

# 🔹 Show columns to help user select
print("\n📊 Available columns in your file:")
print(df.columns.tolist())

# 🔹 Ask user to choose X and Y columns
y = input("Enter the name of the column for Y-axis: ").strip()

# 🔹 Validate selected columns
if y not in df.columns:
    print("❌ Invalid column names.")
    exit()

# 🔹 Function to detect string identifiers (like A3SGXH7AUHU8GW)
def is_id_column(series):
    return series.dtype == object and series.str.match(r'^[A-Za-z0-9]{8,}$').mean() > 0.8

# 🔹 Check for ID-like columns and abort if found
if is_id_column(df[y]):
    print(f"❌ Column '{y}' looks like an ID or product code. Choose a different column.")
    exit()

# 🔹 Define custom month mapping
month_map = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12
}

# 🔹 Clean and encode columns
x=df.columns.tolist()
for col in (x):
    if df[col].dtype == object:
        # Try mapping months
        df[col] = df[col].astype(str).str.lower().map(month_map).fillna(df[col])
        # Label encode remaining strings
        if df[col].dtype == object:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

# 🔹 Convert to numeric safely
for x in x:
    df[x] = pd.to_numeric(df[x], errors='coerce')
df[y] = pd.to_numeric(df[y], errors='coerce')
df = df.dropna()

# Plot Scatter Plot
# plt.figure(figsize=(8, 6))
# sns.scatterplot(data=df, x=x, y=y)
# plt.title(f'Scatter Plot: {x} vs {y}')
# plt.xlabel(x)
# plt.ylabel(y)
# plt.grid(True)
# plt.show()

#  Scatter plots of all other numeric columns vs target column y
numeric_columns = df.columns.tolist()

print(f"\n📉 Generating scatter plots of each column vs '{y}' (excluding '{y}'):")

for col in numeric_columns:
    if col == y:
        continue  # Skip the target column itself
    
    plt.figure(figsize=(9, 7))
    sns.scatterplot(data=df, x=col, y=y)
    plt.title(f'Scatter Plot: {col} vs {y}')
    plt.xlabel(col)
    plt.ylabel(y)
    plt.grid(True)
    plt.tight_layout()
    plt.show()




# 🔹 Bar plots of each non-target column vs target column (Y)
print(f"\n📊 Generating bar plots for each column vs '{y}' (excluding '{y}'):")

for col in df.columns:
    if col == y:
        continue  # Skip target column

    # Skip high-cardinality columns
    if df[col].nunique() > 50:
        print(f"⚠️ Skipping '{col}' - too many unique values for a bar chart.")
        continue

    # Prepare plotting data
    df_plot = df.copy()

    # Convert numeric to string category
    if pd.api.types.is_numeric_dtype(df_plot[col]):
        df_plot[col] = df_plot[col].round(0).astype(int).astype(str)
    else:
        df_plot[col] = df_plot[col].astype(str)

    # Group by column and compute mean of y
    bar_data = df_plot.groupby(col, observed=True)[y].mean().reset_index().sort_values(by=y, ascending=False)

    # Bar Plot
    plt.figure(figsize=(max(8, len(bar_data) * 0.6), 5))  # dynamic width
    sns.barplot(data=bar_data, x=col, y=y)

    plt.title(f'Bar Plot: {col} vs {y}')
    plt.xlabel(col)
    plt.ylabel(f'Average {y}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, axis='y')
    plt.show()

# 🔹 Heatmap of all numeric correlations
correlation_matrix = df.select_dtypes(include='number').corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()

# 🔹 Correlation of Target Column (Y) with All Other Columns
print(f"\n📈 Correlation of '{y}' with all other numeric columns:\n")

target_corr = correlation_matrix[y].drop(labels=[y])  # Exclude self-correlation
target_corr_sorted = target_corr.sort_values(ascending=False)

for col, corr_value in target_corr_sorted.items():
    print(f"{col} ⟶ {corr_value:.2f}")

# 🔹 Interpretation
if corr_value > 0.7:
    print("✅ Strong positive correlation")
elif corr_value > 0.3:
    print("✅ Moderate positive correlation")
elif corr_value > 0:
    print("✅ Weak positive correlation")
elif corr_value < -0.7:
    print("🔻 Strong negative correlation")
elif corr_value < -0.3:
    print("🔻 Moderate negative correlation")
elif corr_value < 0:
    print("🔻 Weak negative correlation")
else:
    print("⚠️ No correlation")
