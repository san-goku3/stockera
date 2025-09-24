#pip install pandas psycopg2-binary openpyxl
#run from within terminal

import pandas as pd
from sqlalchemy import create_engine

# Load the Excel file
file_path = r'E:\BluestockFintech-main\BluestockFintech-main\excel_to_database\data\data.xlsx'
df = pd.read_excel(file_path)

# Create an SQLAlchemy engine
engine = create_engine('postgresql+psycopg2://postgres:root@localhost/bluestock_fintech')

# Write the data to the PostgreSQL table
df.to_sql('admin_app_ipoinfo', engine, if_exists='append', index=False)
