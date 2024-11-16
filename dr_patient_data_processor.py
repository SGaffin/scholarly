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

patient_data_entry = pd.read_excel('C:/Users/steve/OneDrive/Desktop/initial_patient_entry.xlsx')
patient_data_entry = patient_data_entry.reset_index()
patient_data_entry = patient_data_entry.rename(columns = {'index':'patient_id'})

#------------------------
vitals = patient_data_entry[['patient_id','age', 'heart_rate', 'blood_pressure', 'resp_rate', 'O2_sat', 'weight']]
vitals.loc[:,'datetime'] = np.nan

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""CREATE TABLE patient_vitals (patient_id, age, heart_rate, blood_pressure, resp_rate, O2_sat, weight, datetime)""")
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
vitals.to_sql('patient_vitals', conn, if_exists='append', index=False)
conn.commit()
conn.close()
#------------------------

#lab results (steven)----------------------------]
lab_results = pd.read_csv('./data/init_data/Urine_lab_values.csv')
lab_results = lab_results.reset_index()
lab_results = lab_results.rename(columns = {'index':'lab_id'})
#---------------------------------------------------------------

#------------------------
diag_dose = patient_data_entry[['patient_id','diagnosis_1', 'drug_1', 'diagnosis_2', 'drug_2', 'diagnosis_3', 'drug_3', 'diagnosis_4', 'drug_4']]
diag_dose_clean = pd.DataFrame(columns=['patient_id', 'diagnosis', 'drug'])
for i in range(len(diag_dose)):
    temp = pd.DataFrame(columns=['patient_id', 'diagnosis', 'drug'])
    for j in range(4):
        temp.loc[j,'patient_id'] = diag_dose.loc[i,'patient_id']
        temp.loc[j,'diagnosis'] = diag_dose.loc[i,'diagnosis_' + str(j + 1)]
        temp.loc[j,'drug'] = diag_dose.loc[i,'drug_' + str(j + 1)]
    diag_dose_clean = diag_dose_clean._append(temp)
diag_dose_clean = diag_dose_clean[~(diag_dose_clean['diagnosis'].isna())]
diag_dose_clean = diag_dose_clean.reset_index(drop = True)

diag_dose = diag_dose_clean.merge(diagtest, how = 'left', on = ['diagnosis'])
diag_dose = diag_dose.rename(columns = {'id':'diagnosis_id'})
diag_dose = diag_dose.reset_index(drop = True)

diag_dose = diag_dose.merge(drugtest, how = 'left', left_on = ['drug'], right_on = ['drug_name'])
diag_dose = diag_dose.rename(columns={'id':'drug_id'})
diag_dose.loc[:,'notes'] = np.nan
diag_dose.loc[:,'patient_id'] = diag_dose.loc[:,'patient_id'].astype(int)

diag_dose = diag_dose[['patient_id','diagnosis_id', 'drug_id', 'notes']]

conn = sqlite3.connect(db_path)
c = conn.cursor()
# c.execute("""CREATE TABLE patient_diag_drug (patient_id, diagnosis_id, drug_id, notes)""")
# c.execute("""UPDATE patient_diag_drug SET notes = CAST(notes AS TEXT)""")  #example of setting the datatype of column after table has already been created
# c.execute("""DROP TABLE patient_diag_drug""")
conn.commit()
conn.close()

conn = sqlite3.connect(db_path)
diag_dose.to_sql('patient_diag_drug', conn, if_exists='append', index=False)
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
# c.execute("""CREATE TABLE patient_lab_results (patient_id, lab_name, lab_value)""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# lab_results_clean.to_sql('patient_lab_results', conn, if_exists='append', index=False)
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# plr = c.execute('SELECT * FROM patient_lab_results')
# plrdata = pd.DataFrame(c.fetchall())
# cols = list(pd.DataFrame(plr.description)[0])
# plrdata.columns = cols
#------------------------

#------------------------
glasses = patient_data_entry[['patient_id', 'reading_glasses']]
glasses = glasses[~(glasses['reading_glasses'].isna())]

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""CREATE TABLE patient_glasses (patient_id, reading_glasses)""")
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




##example to view data in drug_index table
conn = sqlite3.connect(db_path)
c = conn.cursor()
pv = c.execute('SELECT * FROM patient_vitals')
pvdata = pd.DataFrame(c.fetchall())
cols = list(pd.DataFrame(pv.description)[0])
pvdata.columns = cols
#----------------------------------------------------------------------------------------------------------------

#drug_index initialization---------------------------------------------------------------------------------------
# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""DROP TABLE drug_index""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE drug_index (id, drug_name, dosage, distribution)""")
# ###c.execute("""DELETE FROM drug_index WHERE drug_name = 'Ibuprofen' """)
# ###c.execute("""UPDATE drug_index SET drug_name = 'Enalapril' WHERE drug_name = 'Enalapril '  """)
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# drug.to_sql('drug_index', conn, if_exists='append', index=False)
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
# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE diagnosis_index (id, diagnosis)""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# diagnosis.to_sql('diagnosis_index', conn, if_exists='append', index=False)
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
# diag_meds_cache = diag_meds
# diag_meds = diag_meds.merge(drug, how = 'left', on = ['drug_name','dosage','distribution'])
# diag_meds = diag_meds.rename(columns = {'id':'drug_id'})

# diag_meds = diag_meds.merge(diagnosis, how = 'left', on = ['diagnosis'])
# diag_meds = diag_meds.rename(columns = {'id':'diagnosis_id'})
# diag_meds = diag_meds[['diagnosis_id', 'drug_id', 'dosage', 'distribution']]

# conn = sqlite3.connect(db_path)
# c = conn.cursor()
# c.execute("""CREATE TABLE diagnosis_drug_ref (diagnosis_id, drug_id, dosage, distribution)""")
# conn.commit()
# conn.close()

# conn = sqlite3.connect(db_path)
# diag_meds.to_sql('diagnosis_drug_ref', conn, if_exists='append', index=False)
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
                                 ON ddr.diagnosis_id = diag.id""")
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
                          ON pv.patient_id = pdd.patient_id
                          LEFT JOIN (SELECT patient_id, COUNT(*) AS lab_result_count FROM patient_lab_results GROUP BY patient_id) plr
                          ON pv.patient_id = plr.patient_id""")
    pr_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pr_qry.description)[0])
    pr_data.columns = cols
    
    return(pr_data)
    


