import pandas as pd

# Load the Excel file
df = pd.read_excel('Data\Data Valuasi Polis Asuransi Kesehatan BNI Life - Data Mahasiswa atn. Christian.xlsx')


# Calculate the number of rows to keep
num_rows = len(df)
rows_to_keep = num_rows // 2

# Keep only the first half of the rows
df = df.iloc[:rows_to_keep]

# Save the modified DataFrame back to an Excel file
df.to_excel('sample2.xlsx', index=False)
