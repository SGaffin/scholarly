import pandas as pd
import numpy as np
import sqlite3
import datetime



db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/dr_patient_data_23.db'

conn = sqlite3.connect(db_path)
c = conn.cursor()

diag_drug_qry = c.execute("""SELECT * 
                             FROM patient_diag_drug
                             WHERE CAST(year AS NVARCHAR) = '2025' 
                             ORDER BY CAST(patient_id AS INTEGER)""")

diag_drug_test = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(diag_drug_qry.description)[0])
diag_drug_test.columns = cols

diag_drug_test.loc[:, 'drug_count'] = 1
drug_count = diag_drug_test.copy()
drug_count = drug_count.groupby(['drug_id'], as_index = False).agg({'drug_count':'sum'})


conn = sqlite3.connect(db_path)
c = conn.cursor()

pharm_qry = c.execute("""SELECT * 
                             FROM pharmacy_record
                             WHERE CAST(year AS NVARCHAR) = '2025' 
                             ORDER BY CAST(drug_id AS INTEGER)""")

pharm_qry_data = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(pharm_qry.description)[0])
pharm_qry_data.columns = cols


conn = sqlite3.connect(db_path)
c = conn.cursor()

drug_index_qry = c.execute("""SELECT *
                             FROM drug_index
                             WHERE CAST(year AS NVARCHAR) = '2025' 
                             ORDER BY CAST(id AS INTEGER)""")

drug_index_data = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(drug_index_qry.description)[0])
drug_index_data.columns = cols
drug_index_data = drug_index_data.rename(columns = {'id':'drug_id'})

summary = pharm_qry_data.merge(drug_count, how = 'left', on = ['drug_id'])
summary = summary.merge(drug_index_data[['drug_id', 'drug_name', 'dosage']], how = 'left', on = ['drug_id'])
summary.loc[:, 'ordered'] = summary.loc[:, 'ordered'].str.replace(',', '').astype(float)
summary.loc[:, 'distributed'] = summary.loc[:, 'distributed'].str.replace(',', '').astype(float)

summary.loc[:,'units_distributed'] = summary.loc[:, 'distributed'] * summary.loc[:, 'drug_count']
summary.loc[:,'units_distributed'] = np.where(summary.loc[:,'units_distributed'].isna(), 0, summary.loc[:,'units_distributed'])
summary.loc[:,'units_leftover'] = summary.loc[:,'ordered'] - summary.loc[:,'units_distributed']

summary = summary[['year', 'drug_name', 'dosage', 'ordered', 'distributed', 'drug_count', 'units_distributed', 'units_leftover']]
summary.to_csv('C:/Users/jaett/Documents/GitHub/scholarly/distribution_report.csv', index = False)
