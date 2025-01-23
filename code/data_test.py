import pandas as pd
import numpy as np

# Read data from an Excel file 
df = pd.read_excel('sample2.xlsx')

# ----- Start Missing Value Imputation -------

# Remove rows with '0' values in 'BAYAR' column
df = df[df['BAYAR'] != 0]

# Remove rows with null values in the "JENISKELAMIN" column
df = df[df['JENISKELAMIN'] != 0]

# Remove rows with null values in the "NAMAPENYAKIT" column
df = df[df['NAMAPENYAKIT'] !="-"]
df = df.dropna(subset=['NAMAPENYAKIT'])

# Remove rows with null values 
drop_null = ['JENISKLAIM','BAYAR','KARYAWAN']
df = df.dropna(subset=drop_null)

# Remove the all column
columns_to_drop = ['PERIODE', 'NAMAPESERTA', 'KARYAWAN','KLAIM','TOLAK','NAMAKODE','KELASRAWAT','JUMLAHHARI','KELASRI']
df.drop(columns=columns_to_drop, inplace=True)
df.to_excel('sample1.xlsx', index=False)

# ---- Start Feature Engineering ----
# Add a new column "STATUS" based on the "NOMORPESERTA" column
def get_status(row):
    last_char = row['NOMORPESERTA'][-1]
    if last_char == 'A':
        return '1' #Pasangan
    elif last_char == 'B': 
        return '2'#Anak
    else:
        return '3' #Pegawai


df['STATUS'] = df.apply(get_status, axis=1) 

# Remove the "PERIODE" column
df.drop(columns=['NOMORPESERTA'], inplace=True)

# Calculate the new column "HARGAPREMI", use the claim ratio (80%)
df['HARGAPREMI'] =np.ceil(df['BAYAR'] * (100 / 80))

adjustments = np.random.uniform(-0.1, 0.1, size=len(df))
df['HARGAPREMIPERUSAHAAN'] = df['HARGAPREMI'] + (adjustments * df['HARGAPREMI'])

unique_values = df['NAMAPERUSAHAAN'].unique()
value_to_code = {value: code for code, value in zip(range(1, 616), unique_values)}

value_mapping_JENISKELAMIN = {'L': 1, 'P': 2}
df['JENISKELAMIN'] = df['JENISKELAMIN'].map(value_mapping_JENISKELAMIN).fillna(0)

name_counts_perusahaan = df['NAMAPERUSAHAAN'].value_counts()
name_counts_penyakit = df['NAMAPENYAKIT'].value_counts()
name_counts_klaim = df['JENISKLAIM'].value_counts()

# Create a new column 'Total_Kemunculan' with name counts
df['FREKUENSIPERUSAHAAN'] = df['NAMAPERUSAHAAN'].map(name_counts_perusahaan)
# Create a new column 'Total_Kemunculan' with name counts
df['FREKUENSIPENYAKIT'] = df['NAMAPENYAKIT'].map(name_counts_penyakit)
# Create a new column 'Total_Kemunculan' with name counts
df['FREKUENSIKLAIM'] = df['JENISKLAIM'].map(name_counts_klaim)

# Data after cleaning
df.to_excel('clean_case.xlsx', index=False)
