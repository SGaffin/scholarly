# dr_patient_data_23
import pandas as pd
import numpy as np
import sqlite3

#create database


diag_meds = pd.read_csv('./data/init_data/diagnosis_medicine.csv')
diag_meds = diag_meds.rename(columns = {'Drug Name (generic)':'drug_name', 'dIagnosis':'diagnosis','Dose/dosage form':'dosage', 'Pill Distribution':'distribution'})
drug = diag_meds[['drug_name','dosage', 'distribution']]
drug = drug.drop_duplicates().reset_index().rename(columns={'index':'id'})
diagnosis = pd.DataFrame(diag_meds.loc[:,'diagnosis'].drop_duplicates()).reset_index().rename(columns={'index':'id'})


db_path = r'./data/dr_patient_data_23.db'

#patient records------------------------------------------------------------------------------------------------

# patient_data_entry = pd.read_excel('C:/Users/steve/OneDrive/Desktop/initial_patient_entry.xlsx')
# patient_data_entry = patient_data_entry.reset_index()
# patient_data_entry = patient_data_entry.rename(columns = {'index':'patient_id'})
# patient_data_entry_cache = patient_data_entry
#------------------------


# vitals = pd.DataFrame(columns = ['patient_id','first_name','last_name','age','sex', 'heart_rate', 'blood_pressure', 'resp_rate', 'O2_sat', 'weight','datetime'])
# dummyentry = pd.DataFrame([['0','jane','doe','25','F','68','120/80','16', '98', '125', pd.to_datetime('1/30/1986')]])
# dummyentry.columns = vitals.columns
# vitals = vitals._append(dummyentry)

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# # c.execute("""DROP TABLE patient_vitals """)
# c.execute("""CREATE TABLE patient_vitals (patient_id, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight, datetime)""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# vitals.to_sql('patient_vitals', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
pdd = c.execute('SELECT * FROM patient_vitals')
pdddata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(pdd.description)[0])
pdddata.columns = cols
#------------------------



conn = sqlite3.connect(db_path)
c = conn.cursor()
pdd = c.execute("SELECT * FROM sqlite_master WHERE type='table'")
tbls = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(pdd.description)[0])
tbls.columns = cols
#---------------------------------------------------------------

#------------------------
dummyentry = pd.DataFrame([[0,17,27]], columns = ['patient_id','diagnosis_id', 'drug_id'])
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""CREATE TABLE patient_diag_drug (patient_id, diagnosis_id, drug_id)""")
# c.execute("""DROP TABLE patient_diag_drug""")
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
dummyentry.to_sql('patient_diag_drug', conn, if_exists='append', index=False)
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
pdd = c.execute('SELECT * FROM patient_diag_drug')
pdddata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(pdd.description)[0])
pdddata.columns = cols

#------------------------

# #quick fix to missing ref table values
# diag_dose_missing = diag_dose[(diag_dose['diagnosis_id'].isna()) | (diag_dose['drug_id'].isna())]

# drug_missing = diag_dose[(diag_dose['drug_id'].isna())]
# drug_missing = drug_missing[['drug', 'dosage', 'distribution']].drop_duplicates().reset_index(drop=True).reset_index()
# drug_missing = drug_missing.rename(columns = {'index':'id', 'drug':'drug_name'})

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# drug_qry = c.execute('SELECT MAX(id) as drug_id FROM drug_index')
# drugid = pd.DataFrame(c.fetchall())
# cols = list(pd.DataFrame(drug_qry.description)[0])
# drugid.columns = cols

# drugid = drugid.loc[0,'drug_id'] + 1

# drug_missing.loc[:,'id'] = drug_missing.loc[:,'id'] + drugid

# conn = sqlite3.connect(db_path)
# drug_missing.to_sql('drug_index', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()


# diag_missing = diag_dose[(diag_dose['diagnosis_id'].isna())]
# diag_missing = diag_missing[['diagnosis']].drop_duplicates().reset_index(drop=True).reset_index()
# diag_missing = diag_missing.rename(columns = {'index':'id'})

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# diag_qry = c.execute('SELECT MAX(id) as diagnosis_id FROM diagnosis_index')
# diagid = pd.DataFrame(c.fetchall())
# cols = list(pd.DataFrame(diag_qry.description)[0])
# diagid.columns = cols

# diagid = diagid.loc[0,'diagnosis_id'] + 1

# diag_missing.loc[:,'id'] = diag_missing.loc[:,'id'] + diagid

# conn = sqlite3.connect(db_path)
# diag_missing.to_sql('diagnosis_index', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()


#------------------------


#------------------------
#lab results (steven)----------------------------]
# lab_results = pd.read_csv('./data/init_data/Urine_lab_values.csv')
# lab_results = lab_results.rename(columns = {'Test':'lab_name', 'Result':'lab_value'})

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE lab_results_index (lab_id, lab_name, lab_value)""")
# # c.execute("""DROP TABLE lab_results_index""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# lab_results.to_sql('lab_results_index', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
lri = c.execute('SELECT * FROM lab_results_index')
lridata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(lri.description)[0])
lridata.columns = cols


# lab_results = patient_data_entry[['patient_id','Lab_Result_1','Lab_Result_2','Lab_Result_3']]
# lab_results_clean = pd.DataFrame(columns=['patient_id', 'lab_name', 'lab_value'])
# for i in range(len(lab_results)):
#     temp = pd.DataFrame(columns=['patient_id', 'lab_name', 'lab_value'])
#     for j in range(3):
#         temp.loc[j,'patient_id'] = lab_results.loc[i,'patient_id']
#         temp.loc[j,'lab_name'] = lab_results.loc[i,'Lab_Result_' + str(j + 1)]
#         temp.loc[j,'lab_value'] = np.nan
#     lab_results_clean = lab_results_clean._append(temp)
# lab_results_clean = lab_results_clean[~(lab_results_clean['lab_name'].isna())]
# lab_results_clean = lab_results_clean.reset_index(drop = True)
# lab_results_clean.loc[:,'patient_id'] = lab_results_clean.loc[:,'patient_id'].astype(int) 


# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE patient_lab_results (patient_id, lab_id, lab_value)""")
# # c.execute("""DROP TABLE patient_lab_results""")
# conn.commit()
# conn.close()

# dummyentry=pd.DataFrame([[0,5,1.025]],columns=['patient_id', 'lab_id', 'lab_value'])

# conn = sqlite3.connect(db_path)
# dummyentry.to_sql('patient_lab_results', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
plr = c.execute('SELECT * FROM patient_lab_results')
plrdata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(plr.description)[0])
plrdata.columns = cols

#------------------------

#------------------------
glasses = patient_data_entry[['patient_id', 'reading_glasses']]
glasses = glasses[~(glasses['reading_glasses'].isna())]

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""DELETE FROM patient_glasses where patient_id != 0""")
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
glasses.to_sql('patient_glasses', conn, if_exists='append', index=False)
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
gl = c.execute('SELECT * FROM patient_glasses')
gldata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(gl.description)[0])
gldata.columns = cols
#------------------------

#------------------------
dummyentry = pd.DataFrame([[0, 'test procs', 'test notes']],columns=['patient_id', 'procs', 'notes'])

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""CREATE TABLE patient_procs_notes (patient_id, procs, notes)""")
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
dummyentry.to_sql('patient_procs_notes', conn, if_exists='append', index=False)
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
ppn = c.execute('SELECT * FROM patient_procs_notes')
ppndata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(ppn.description)[0])
ppndata.columns = cols
#------------------------




##example to view data in drug_index table
conn = sqlite3.connect(db_path)
c = conn.cursor()
pv = c.execute('SELECT * FROM patient_vitals')
pvdata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(pv.description)[0])
pvdata.columns = cols
#----------------------------------------------------------------------------------------------------------------

#drug_index initialization---------------------------------------------------------------------------------------

drug_read = pd.read_csv('C:/Users/jaett/Documents/GitHub/scholarly/data/init_data/Drug_table.csv')
drug_read.columns = ['id','drug_name','dosage']
# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""DROP TABLE drug_index""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# # c.execute("""CREATE TABLE drug_index (id, drug_name, dosage)""")
# ###c.execute("""DELETE FROM drug_index WHERE drug_name = 'Ibuprofen' """)
# c.execute("""UPDATE drug_index SET drug_name = 'Ibuprofen' WHERE drug_name = 'Ibuprofen '  """)
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# drug_read.to_sql('drug_index', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

##example to view data in drug_index table
conn = sqlite3.connect(db_path)
c = conn.cursor()
drug_qry = c.execute("""SELECT * FROM drug_index""") #  WHERE drug_name = 'SMP/TMX DS' and dosage = 'Kids- ½ tab'
drugtest = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(drug_qry.description)[0])
drugtest.columns = cols
#----------------------------------------------------------------------------------------------------------------


#diagnosis_index initialization----------------------------------------------------------------------------------
diag_read = pd.read_csv('C:/Users/jaett/Documents/GitHub/scholarly/data/init_data/diagnosis_id_table.csv')
diag_read.columns = ['id','diagnosis']

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE diagnosis_index (id, diagnosis)""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# diag_read.to_sql('diagnosis_index', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

##example to view data in drug_index table
conn = sqlite3.connect(db_path)
c = conn.cursor()
diag_qry = c.execute('SELECT * FROM diagnosis_index')
diagtest = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(diag_qry.description)[0])
diagtest.columns = cols
#----------------------------------------------------------------------------------------------------------------


#diagnosis_drug_ref initialization-------------------------------------------------------------------------------
diag_drug_read = pd.read_csv('C:/Users/jaett/Documents/GitHub/scholarly/data/init_data/diag_drug_table.csv')
diag_drug_read.columns = ['diag_id','drug_id']

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE diagnosis_drug_ref (diag_id, drug_id)""")
# # c.execute("""DROP TABLE diagnosis_drug_ref""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# diag_drug_read.to_sql('diagnosis_drug_ref', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

conn = sqlite3.connect(db_path)
c = conn.cursor()
diag_drug_qry = c.execute('SELECT * FROM diagnosis_drug_ref')
diag_drug_test = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(diag_drug_qry.description)[0])
diag_drug_test.columns = cols
#----------------------------------------------------------------------------------------------------------------

#master join-----------------------------------------------------------------------------------------------------

conn = sqlite3.connect(db_path)
c = conn.cursor()
diag_drug_qry = c.execute("""SELECT * 
                             FROM diagnosis_drug_ref ddr
                             LEFT JOIN(SELECT * FROM drug_index) drg
                             ON ddr.drug_id = drg.id""")
diag_drug_test = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(diag_drug_qry.description)[0])
diag_drug_test.columns = cols


def diagdrug_pull():
    
    db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    diag_drug_qry = c.execute("""SELECT * 
                                 FROM diagnosis_drug_ref ddr
                                 LEFT JOIN(SELECT * FROM drug_index) drg
                                 ON ddr.drug_id = drg.id
                                 LEFT JOIN(SELECT * FROM diagnosis_index) diag
                                 ON ddr.diag_id = diag.id""")
    diag_drug_test = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(diag_drug_qry.description)[0])
    diag_drug_test.columns = cols
    
    return(diag_drug_test)
    
def patientrecord_pull():
    
    db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    pr_qry = c.execute("""SELECT pv.*, pdd.diag_count, plr.lab_result_count
                          FROM patient_vitals pv
                          LEFT JOIN(SELECT patient_id, COUNT(*) AS diag_count FROM patient_diag_drug GROUP BY patient_id) pdd
                          ON CAST(pv.patient_id AS INT) = CAST(pdd.patient_id AS INT)
                          LEFT JOIN (SELECT patient_id, COUNT(*) AS lab_result_count FROM patient_lab_results GROUP BY patient_id) plr
                          ON CAST(pv.patient_id AS INT) = CAST(plr.patient_id AS INT)""")
    pr_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pr_qry.description)[0])
    pr_data.columns = cols
    
    return(pr_data)
    


