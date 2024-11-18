import pandas as pd
import numpy as np
import sqlite3
import datetime


def diagdrug_pull():
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
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
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
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

def patient_vitals_staging(first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_vitals_temp""")
        conn.commit()
        conn.close()
    except:
        print('temp vitals table did not exist')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE patient_vitals_temp (patient_id, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight, datetime)""")
    conn.commit()
    conn.close()
    
    pv_temp = pd.DataFrame([[0, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight,datetime.date.today()]],
                           columns = ['patient_id','first_name','last_name','age','sex', 'heart_rate', 'blood_pressure', 'resp_rate', 'O2_sat', 'weight','datetime'])

    conn = sqlite3.connect(db_path)
    pv_temp.to_sql('patient_vitals_temp', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    return(pv_temp)


def diag_drug_staging(diagnosis, drug, procs, notes):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_diag_drug_temp""")
        conn.commit()
        conn.close()
    except:
        print('temp patient_diag_drug table did not exist')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE patient_diag_drug_temp (patient_id, diagnosis_id, drug_id, procs, notes)""")
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    di = c.execute("""SELECT * FROM diagnosis_index WHERE diagnosis = """ + diagnosis)
    didata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(di.description)[0])
    didata.columns = cols
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    dri = c.execute("""SELECT * FROM drug_index WHERE drug_name = """ + drug)
    dridata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(dri.description)[0])
    dridata.columns = cols
    
    ddt = pd.DataFrame([[0, diagnosis, drug, procs, notes]], columns = ['patient_id', 'diagnosis', 'drug', 'procs', 'notes'])
    ddt = ddt.merge(didata, how = 'left', on = ['diagnosis'])
    ddt = ddt.merge(dridata, how = 'left', left_on = ['drug'], right_on = ['drug_name'])
    
    ddt = ddt[['patient_id', 'diagnosis_id', 'drug_id', 'procs', 'notes']]

    conn = sqlite3.connect(db_path)
    ddt.to_sql('patient_diag_drug_temp', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    return(ddt)



