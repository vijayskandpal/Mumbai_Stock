import streamlit as st
import pandas as pd


FilePath = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT-g-e-JRzeuReeaIvjf6bSFtLTu5PQBQjtKq5uT2R1Wq5XS9oiOLHlC59JNok3TajZ4fvnbSUJO4nI/pub?output=xlsx'
#st.sidebar.success("Select a demo above.")
df_data = pd.read_excel(FilePath,sheet_name='DATA', usecols=range(0,10))
df_data.rename(columns={'Bill / Inv No /Faulty/Sample': 'INV'}, inplace=True)

# Downcast numeric types
numeric_columns = df_data.select_dtypes(include=['int64', 'float64']).columns
df_data[numeric_columns] = df_data[numeric_columns].apply(pd.to_numeric, downcast='unsigned')

# Convert object types to categorical
object_columns = df_data.select_dtypes(include=['object']).columns
df_data[object_columns] = df_data[object_columns].astype('category')

#st.dataframe(df_data)
df_clstk = pd.read_excel(FilePath,sheet_name='Item_List', usecols=range(0,11))
df_clstk = df_clstk.drop(columns=['Box Location', 'Physical Date','Net'])
Total_stock = df_clstk['QTY'].sum()

st.title(f"Total Closing Stock Items :  {Total_stock}")

df_max = df_clstk.iloc[:,[0,2,6,7]]
df_max = df_max[(df_max['QTY'] > 0) & (df_max['MAX QTY'] > 0) & 
        (df_max['QTY'] > df_max['MAX QTY'])].sort_values(by=('QTY'),
        ascending=False).reset_index(drop=True)
st.dataframe(df_max)

# with col2:
df_min = df_clstk.iloc[:,[0,2,5,7]]
df_min = df_min[(df_min['QTY'] > 0) & (df_min['MIN QTY'] > 0) & 
        (df_min['QTY'] < df_min['MIN QTY'])].sort_values(by=('QTY'),
        ascending=False).reset_index(drop=True)
st.dataframe(df_min)
