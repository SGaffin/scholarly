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
        print('patient_lab_results_temp did not exist')
    
    
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
    # pr_qry = c.execute("""SELECT pv.*, pdd.diagnosis_id, pdd.drug_id, plr.lab_id, plr.lab_value, pg.reading_glasses
    #                       FROM patient_vitals pv
    #                       LEFT JOIN(SELECT patient_id, diagnosis_id, drug_id FROM patient_diag_drug) pdd
    #                       ON pv.patient_id = pdd.patient_id
    #                       LEFT JOIN (SELECT patient_id, lab_id, lab_value FROM patient_lab_results) plr
    #                       ON pv.patient_id = plr.patient_id
    #                       LEFT JOIN (SELECT patient_id, reading_glasses  FROM patient_glasses GROUP BY patient_id) pg
    #                       ON pv.patient_id = plr.patient_id
    #                       ORDER BY CAST(pv.patient_id AS INT)""")
    
    pr_qry = c.execute("""SELECT pv.*
                          FROM patient_vitals pv""")
                      
    pr_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pr_qry.description)[0])
    pr_data.columns = cols
    
    return(pr_data)

def diagdrug_recordviewer():
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()    
    dd_qry = c.execute("""SELECT first_name, last_name, diagnosis, drug_name
                          FROM patient_diag_drug pdd
                          
                          LEFT JOIN(SELECT DISTINCT patient_id, first_name, last_name
                                    FROM patient_vitals) pv
                          ON CAST(pdd.patient_id AS INT) = CAST(pv.patient_id AS INT)

                        LEFT JOIN(SELECT *
                                  FROM diagnosis_index) di
                        ON pdd.diagnosis_id = di.id
                        LEFT JOIN(SELECT *
                                  FROM drug_index) dri
                        ON pdd.drug_id = dri.id
                        
                        ORDER BY CAST(pdd.patient_id AS INT), last_name, first_name""")
                      
    dd_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(dd_qry.description)[0])
    dd_data.columns = cols
    
    return (dd_data)

def pharm_recordviewer(yr):
    
    try:
        yr = str(yr)
    except:
        print('yr is already a string')
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor() 
    
    pharm_qry = c.execute("""SELECT *
                             FROM pharmacy_record pr
                             LEFT JOIN(SELECT *
                                       FROM drug_index) dri
                             ON pr.drug_id = dri.id
                             WHERE year = """ + yr)
    pharm_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pharm_qry.description)[0])
    pharm_data.columns = cols
    
    pharm_data_ret = pharm_data[['year', 'drug_name', 'dosage', 'ordered', 'distributed']]
    
    return(pharm_data_ret)

def pharm_years():
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor() 
    
    yrs_qry = c.execute("""SELECT DISTINCT year
                             FROM pharmacy_record
                             ORDER BY year""")
    yrs = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(yrs_qry.description)[0])
    yrs.columns = cols
    
    yrs = list(yrs.loc[:,'year'])
    
    return(yrs)

def pharm_update_staging(pr_edit):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    pr_edit = pd.DataFrame(pr_edit)
    pr_edit.loc[:,'stage_update'] = pd.to_datetime(datetime.datetime.now())

    
    try:
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor() 
        pharmstage_qry = c.execute("""SELECT *
                                      FROM pharmacy_staging""")
        pharmstage = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pharmstage_qry.description)[0])
        pharmstage.columns = cols
        
        pharmstage.loc[:,'stage_update'] = pd.to_datetime(pharmstage.loc[:,'stage_update'])
        
    except:
        pharmstage = pd.DataFrame()
    
    staging_update = pharmstage._append(pr_edit)
    staging_update = staging_update.sort_values(by = ['stage_update'], ascending = True)
    staging_update = staging_update.drop_duplicates(keep='first')
    
    conn = sqlite3.connect(db_path)
    staging_update.to_sql('pharmacy_staging', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()


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


def diag_drug_staging(diagnosis, drug):
    
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
        c.execute("""CREATE TABLE patient_diag_drug_temp (patient_id, diagnosis_id, drug_id)""")
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
    
    ddt = pd.DataFrame([[0, diagnosis, drug]], columns = ['patient_id', 'diagnosis', 'drug'])
    ddt = ddt.merge(didata, how = 'left', on = ['diagnosis'])
    ddt = ddt.merge(dridata, how = 'left', left_on = ['drug'], right_on = ['drug_name'])
    
    ddt_return = ddt[['diagnosis', 'drug']]
    ddt = ddt[['patient_id', 'diagnosis_id', 'drug_id']]

    conn = sqlite3.connect(db_path)
    ddt.to_sql('patient_diag_drug_temp', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    ddtc = c.execute("""SELECT diagnosis, drug_name AS drug
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


def final_submit(fname, lname, age, sex, weight, hr, bp, rr, o2sat, procs, notes, glasses):
    
    db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    pdd = c.execute('SELECT MAX(CAST(patient_id AS INT)) as last_id FROM patient_vitals')
    pdddata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pdd.description)[0])
    pdddata.columns = cols
    
    patient_id = int(pdddata.loc[0,'last_id']) + 1
    
    #patient vitals section-------------------------------------------------------------
    dt = pd.to_datetime('now').strftime("%Y-%m-%d %H:%M:%S")
    
    pv = pd.DataFrame([[patient_id, fname, lname, age, sex, hr, bp, rr, o2sat, weight, dt]], 
                      columns = ['patient_id', 'first_name', 'last_name', 'age', 'sex', 'heart_rate', 'blood_pressure', 'resp_rate', 'O2_sat', 'weight','datetime'])
    

    conn = sqlite3.connect(db_path)
    pv.to_sql('patient_vitals', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    

    #patient lab results section--------------------------------------------------------
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        lrt = c.execute('SELECT * FROM patient_lab_results_temp')
        lrtdata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(lrt.description)[0])
        lrtdata.columns = cols
    
        lrtdata.loc[:,'patient_id'] = patient_id
        
        conn = sqlite3.connect(db_path)
        lrtdata.to_sql('patient_lab_results', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()    

    except:
        print("No labs performed")
    
    #patient diagnosis & drug section----------------------------------------------------
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    pdd = c.execute('SELECT * FROM patient_diag_drug_temp')
    pdddata = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pdd.description)[0])
    pdddata.columns = cols
    
    pdddata.loc[:,'patient_id'] = patient_id
    
    conn = sqlite3.connect(db_path)
    pdddata.to_sql('patient_diag_drug', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    #patient procedures and notes section----------------------------------------------------
    
    ppn = pd.DataFrame([[patient_id, procs, notes]], columns = ['patient_id', 'procs', 'notes'])
    
    conn = sqlite3.connect(db_path)
    ppn.to_sql('patient_procs_notes', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    #patient glasses section ----------------------------------------------------------------
    if glasses != 'No Glasses':
        glasses = pd.DataFrame([[patient_id, glasses]], columns = ['patient_id', 'reading_glasses'])
        
        conn = sqlite3.connect(db_path)
        glasses.to_sql('patient_glasses', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()

    success_text = 'Patient has been submitted to system.'

    return(success_text)
    
    
    
    # DELETE FROM patient_vitals WHERE patient_id = 1
    # DELETE FROM patient_lab_results WHERE patient_id = 1
    # DELETE FROM patient_diag_drug WHERE patient_id = 1
    # DELETE FROM patient_procs_notes WHERE patient_id = 1
    # DELETE FROM patient_glasses WHERE patient_id = 1

    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_vitals WHERE CAST(patient_id AS INT)>= 1""")
    # conn.commit()
    # conn.close()
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_lab_results WHERE CAST(patient_id AS INT) >= 1""")
    # conn.commit()
    # conn.close()
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_diag_drug WHERE CAST(patient_id AS INT) >= 1""")
    # conn.commit()
    # conn.close()  
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_procs_notes WHERE CAST(patient_id AS INT) >= 1""")
    # conn.commit()
    # conn.close()      
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_glasses WHERE CAST(patient_id AS INT) >= 1""")
    # conn.commit()
    # conn.close()          
    