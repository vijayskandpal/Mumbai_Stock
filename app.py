"""Module providing a function printing python version."""
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Mumbai Stock",
    layout='centered'
)

FilePath = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT-g-e-JRzeuReeaIvjf6bSFtLTu5PQBQjtKq5uT2R1Wq5XS9oiOLHlC59JNok3TajZ4fvnbSUJO4nI/pub?output=xlsx'
#FILEPATH = r'mh-stock.xlsx'
#st.sidebar.success("Select a demo above.")
df_data = pd.read_excel(FILEPATH,sheet_name='DATA', usecols=range(0,10))
df_data.rename(columns={'Bill / Inv No /Faulty/Sample': 'INV'}, inplace=True)

# Downcast numeric types
numeric_columns = df_data.select_dtypes(include=['int64', 'float64']).columns
df_data[numeric_columns] = df_data[numeric_columns].apply(pd.to_numeric, downcast='unsigned')

# Convert object types to categorical
object_columns = df_data.select_dtypes(include=['object']).columns
df_data[object_columns] = df_data[object_columns].astype('category')
df_data['INV'] = df_data['INV'].astype('object')
df_data['Remarks'] = df_data['Remarks'].astype('object')
df_data.reset_index(drop=True)

#st.dataframe(df_data)
df_clstk = pd.read_excel(FILEPATH,sheet_name='Item_List', usecols=range(0,11))
df_clstk = df_clstk.drop(columns=['Box Location', 'Physical Date','Net'])
Total_stock = df_clstk['QTY'].sum()
df_clstk.sort_values(by=['Category','BRAND','QTY'],ascending=[False,False,False],inplace=True)
Available_Stock = df_clstk.loc[:,['Item_Code','QTY','Particulars']]
Available_Stock = Available_Stock[Available_Stock['QTY'] > 0].reset_index(drop=True)

current_datetime = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
st.header(f"Total Closing Stock Items :  {Total_stock} as on {current_datetime}")

st.subheader("Available Stock Items")
st.table(Available_Stock)

st.subheader("Available Vs Max")
df_max = df_clstk.iloc[:,[0,2,6,7]]
df_max = df_max[(df_max['QTY'] > 0) & (df_max['MAX QTY'] > 0) & (df_max['QTY'] > df_max['MAX QTY'])]
df_max.sort_values(by=('QTY'),ascending=False).reset_index(drop=True)
st.table(df_max)


st.subheader("Available Vs Min")
df_min = df_clstk.iloc[:,[0,2,5,7]]
df_min = df_min[(df_min['QTY'] != 0) & (df_min['MIN QTY'] != 0) & (df_min['QTY'] < df_min['MIN QTY'])].reset_index(drop=True)
df_max.sort_values(by=('QTY'), ascending=False)
st.table(df_min)

st.subheader("Last Outward 3 Days")
last_outward = df_data.iloc[:,[0,1,2,3,4,5,6,7]]
last_outward = last_outward[(last_outward['IN/OUT'] == 'OUT')]
last_outward.sort_values(by=['Mtrl_InOut_Date','INV'],ascending=[False,False],inplace=True)
day_1 = datetime.today() - timedelta(days=3)
last_outward = last_outward[last_outward['Mtrl_InOut_Date'] > day_1].reset_index(drop=True)
# Convert string columns to datetime
last_outward['Mtrl_InOut_Date'] = pd.to_datetime(last_outward['Mtrl_InOut_Date'])
last_outward['BILL_DATE'] = pd.to_datetime(last_outward['BILL_DATE'])
# Format date columns as strings in "dd/mm/yyyy" format
last_outward['Mtrl_InOut_Date'] = last_outward['Mtrl_InOut_Date'].dt.strftime('%d/%m/%Y')
last_outward['BILL_DATE'] = last_outward['BILL_DATE'].dt.strftime('%d/%m/%Y')
last_outward.drop(columns=['IN/OUT'],inplace=True)
st.table(last_outward)

st.subheader("Last Inward 3 Days")
last_outward = df_data.iloc[:,[0,1,2,3,4,5,6,7]]
last_outward = last_outward[(last_outward['IN/OUT'] == 'IN')]
last_outward.sort_values(by=['Mtrl_InOut_Date','INV'],ascending=[False,False],inplace=True)
day_1 = datetime.today() - timedelta(days=3)
last_outward = last_outward[last_outward['Mtrl_InOut_Date'] > day_1].reset_index(drop=True)
# Convert string columns to datetime
last_outward['Mtrl_InOut_Date'] = pd.to_datetime(last_outward['Mtrl_InOut_Date'])
last_outward['BILL_DATE'] = pd.to_datetime(last_outward['BILL_DATE'])
# Format date columns as strings in "dd/mm/yyyy" format
last_outward['Mtrl_InOut_Date'] = last_outward['Mtrl_InOut_Date'].dt.strftime('%d/%m/%Y')
last_outward['BILL_DATE'] = last_outward['BILL_DATE'].dt.strftime('%d/%m/%Y')
last_outward.drop(columns=['IN/OUT'],inplace=True)
st.table(last_outward)
# End-of-file (EOF)
# Display table with custom CSS
st.write(
    f"""
    <style>
        table {{border-collapse: collapse; width: 100%;}}
        th, td {{ text-align: left; padding: 8px; }}
        th {{ background-color: #f2f2f2; color: #000000; font-weight: bold; }}
        td {{ border-bottom: 2px solid #dddddd; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #ddd; }}
    </style>
    """
    , unsafe_allow_html=True
)
