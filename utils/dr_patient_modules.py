import pandas as pd
import numpy as np
import sqlite3
import datetime

def cleartemps():
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_vitals_temp""")
        conn.commit()
        conn.close()
    except:
        print('patient_vitals_temp did not exist')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_diag_drug_temp""")
        conn.commit()
        conn.close()
    except:
        print('patient_diag_drug_temp did not exist')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_lab_results_temp""")
        conn.commit()
        conn.close()
    except:
        print('patient_diag_drug_temp did not exist')
    
    
    r = 'temp tables dropped'
    
    return(r)


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


def lab_tests_pull():
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lab_res_qry = c.execute("""SELECT * 
                                 FROM lab_results_index""")
    lab_res = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lab_res_qry.description)[0])
    lab_res.columns = cols
    
    return(lab_res)
    

    
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
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    pv = c.execute("""SELECT * FROM patient_vitals_temp""")
    pv_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pv.description)[0])
    pv_return.columns = cols
    
    return(pv_return)


def diag_drug_staging(diagnosis, drug, procs, notes):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    # try:
    #     conn = sqlite3.connect(db_path)
    #     c = conn.cursor()
    #     c.execute("""DROP TABLE patient_diag_drug_temp""")
    #     conn.commit()
    #     conn.close()
    # except:
    #     print('temp patient_diag_drug table did not exist')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE patient_diag_drug_temp (patient_id, diagnosis_id, drug_id, procs, notes)""")
        conn.commit()
        conn.close()
    except: 
        print('temp patient_diag_drug table already exists')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    di = c.execute("""SELECT id AS diagnosis_id, diagnosis FROM diagnosis_index WHERE diagnosis = '""" + str(diagnosis) + """'""")
    didata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(di.description)[0])
    didata.columns = cols
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    dri = c.execute("""SELECT id AS drug_id, drug_name FROM drug_index WHERE drug_name = '""" + str(drug) + """'""")
    dridata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(dri.description)[0])
    dridata.columns = cols
    
    ddt = pd.DataFrame([[0, diagnosis, drug, procs, notes]], columns = ['patient_id', 'diagnosis', 'drug', 'procs', 'notes'])
    ddt = ddt.merge(didata, how = 'left', on = ['diagnosis'])
    ddt = ddt.merge(dridata, how = 'left', left_on = ['drug'], right_on = ['drug_name'])
    
    ddt_return = ddt[['diagnosis', 'drug', 'procs', 'notes']]
    ddt = ddt[['patient_id', 'diagnosis_id', 'drug_id', 'procs', 'notes']]

    conn = sqlite3.connect(db_path)
    ddt.to_sql('patient_diag_drug_temp', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    ddtc = c.execute("""SELECT diagnosis, drug_name AS drug, procs, notes
                        FROM patient_diag_drug_temp ddt
                        LEFT JOIN(SELECT *
                                  FROM diagnosis_index) di
                        ON ddt.diagnosis_id = di.id
                        LEFT JOIN(SELECT *
                                  FROM drug_index) dri
                        ON ddt.drug_id = dri.id""")
    ddt_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(ddtc.description)[0])
    ddt_return.columns = cols
    
    # ddt_return = pd.DataFrame([[diagnosis, drug, procs, notes]])
    
    return(ddt_return)

def lab_results_staging(lab_name, lab_value):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
        
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE patient_lab_results_temp (patient_id, lab_id, lab_value)""")
        conn.commit()
        conn.close()
    except: 
        print('temp patient_lab_results table already exists')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lri = c.execute("""SELECT DISTINCT lab_id, lab_name FROM lab_results_index WHERE lab_name = '""" + str(lab_name) + """'""")
    lridata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lri.description)[0])
    lridata.columns = cols
    
    lrt = pd.DataFrame([[0, lab_name, lab_value]], columns = ['patient_id', 'lab_name', 'lab_value'])
    lrt = lrt.merge(lridata, how = 'left', on = ['lab_name'])
    lrt = lrt[['patient_id', 'lab_id', 'lab_value']]

    conn = sqlite3.connect(db_path)
    lrt.to_sql('patient_lab_results_temp', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lrtc = c.execute("""SELECT lab_name, lrt.lab_value
                        FROM patient_lab_results_temp lrt
                        LEFT JOIN(SELECT DISTINCT lab_id, lab_name
                                  FROM lab_results_index) lri
                        ON lrt.lab_id = lri.lab_id""")
    lrt_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lrtc.description)[0])
    lrt_return.columns = cols
    
    # ddt_return = pd.DataFrame([[diagnosis, drug, procs, notes]])
    
    return(lrt_return)



