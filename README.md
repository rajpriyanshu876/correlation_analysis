# 📊 Correlation Analysis Tool (CSV/Excel)

This Python-based project helps you analyze the correlation between a **target column** and all other features in your dataset. It supports both **CSV** and **Excel** files and provides insightful **visualizations** like scatter plots, bar charts, and heatmaps.

---

## 🔧 Features

- Upload `.csv`, `.xlsx`, or `.xls` files via a file dialog
- Automatically encode string columns (like months) into numeric format
- Skip product IDs or unique identifiers intelligently
- Generate:
  - ✅ Bar plots for each column vs target
  - ✅ Scatter plots for each column vs target
  - ✅ Correlation matrix heatmap
  - ✅ Correlation score between target and all numeric features

---

## 🚀 How to Run

1. Make sure you have Python installed (>=3.7)
2. Install required libraries:
   ```bash
   pip install pandas seaborn matplotlib scikit-learn openpyxl

3. Run the script:
python correlation_analysis.py

4. Follow the prompts:

. Select your dataset file

. Enter the name of the target column (e.g., Sales, Rating, etc.)


📂 Sample Input Format
csv
Copy
Edit
Month, Sales, Profit
January, 2000, 300
February, 2500, 400
...
The script will convert month names like "January" into 1, "February" into 2, etc.

📈 Visual Outputs
Bar Plot – Average target column value per feature

Scatter Plot – Visual trends between numeric features and the target

Heatmap – Correlation matrix of all numeric variables

Correlation Score – Printed for each feature vs target

🛠️ Built With
Python

Pandas

Seaborn & Matplotlib

Scikit-learn

Tkinter (for GUI-based file selection)

