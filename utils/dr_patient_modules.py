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

def patient_vitals_staging(patient_id, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE patient_vitals_temp (patient_id, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight, datetime)""")
    # c.execute("""UPDATE patient_diag_drug SET notes = CAST(notes AS TEXT)""")  #example of setting the datatype of column after table has already been created
    # c.execute("""DELETE FROM patient_diag_drug where patient_id != 0""")
    conn.commit()
    conn.close()
    
    
    today = datetime.date.today()
    pv_temp = pd.DataFrame([[patient_id, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight,pd.to_datetime()]])

    # conn = sqlite3.connect(db_path)
    # diag_dose.to_sql('patient_diag_drug', conn, if_exists='append', index=False)
    # conn.commit()
    # conn.close()

    
    # # db_path = r'./data/dr_patient_data_23.db'
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # pr_qry = c.execute("""SELECT pv.*, pdd.diag_count, plr.lab_result_count
    #                       FROM patient_vitals pv
    #                       LEFT JOIN(SELECT patient_id, COUNT(*) AS diag_count FROM patient_diag_drug GROUP BY patient_id) pdd
    #                       ON pv.patient_id = pdd.patient_id
    #                       LEFT JOIN (SELECT patient_id, COUNT(*) AS lab_result_count FROM patient_lab_results GROUP BY patient_id) plr
    #                       ON pv.patient_id = plr.patient_id""")
    # pr_data = pd.DataFrame(c.fetchall())
    # cols = list(pd.DataFrame(pr_qry.description)[0])
    # pr_data.columns = cols
    
    return(pr_data)