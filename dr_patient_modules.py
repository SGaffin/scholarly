import pandas as pd
import sqlite3
import datetime

def cleartemps(db_path, userid):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_vitals_""" + userid)
        conn.commit()
        conn.close()
    except:
        print('patient_vitals_temp did not exist')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_diag_drug_""" + userid)
        conn.commit()
        conn.close()
    except:
        print('patient_diag_drug_temp did not exist')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_lab_results_""" + userid)
        conn.commit()
        conn.close()
    except:
        print('patient_lab_results_temp did not exist')    
        
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE selected_lab_""" + userid)
        conn.commit()
        conn.close()
    except:
        print('selected_lab_temp did not exist')  

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE selected_diagnosis_""" + userid)
        conn.commit()
        conn.close()
    except:
        print('selected_diagnosis_temp did not exist')  

    r = 'temp tables dropped'
    
    return(r)

def clear_pharm(db_path):
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE pharmacy_staging""")
        conn.commit()
        conn.close()
    except:
        print('pharmacy_staging did not exist') 
        
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE diag_drug_ref_stage""")
        conn.commit()
        conn.close()
    except:
        print('diag_drug_ref_stage did not exist')
    
    r = 'pharm tables dropped'
    
    return(r)


def diagdrug_pull(yr, db_path):
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    diag_drug_qry = c.execute("""SELECT * 
                                 FROM diagnosis_drug_ref ddr
                                 LEFT JOIN(SELECT * FROM drug_index) drg
                                 ON CAST(ddr.drug_id AS INTEGER) = CAST(drg.id AS INTEGER) and CAST(ddr.year AS NVARCHAR)= CAST(drg.year AS NVARCHAR)
                                 LEFT JOIN(SELECT * FROM diagnosis_index) diag
                                 ON CAST(ddr.diag_id AS INTEGER) = CAST(diag.id AS INTEGER) and CAST(ddr.year AS NVARCHAR) = CAST(diag.year AS NVARCHAR)
                                 WHERE CAST(ddr.year AS NVARCHAR) = """ + str(yr) )
    diag_drug_test = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(diag_drug_qry.description)[0])
    diag_drug_test.columns = cols
    
    return(diag_drug_test)


def lab_tests_pull(db_path):
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lab_res_qry = c.execute("""SELECT * 
                                 FROM lab_results_index""")
    lab_res = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lab_res_qry.description)[0])
    lab_res.columns = cols
    
    return(lab_res)
    

    
def patientrecord_pull(yr, db_path):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
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
                          FROM patient_vitals pv
                          WHERE CAST(year AS NVARCHAR) = '""" + str(yr) +"""'""")
                      
    pr_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pr_qry.description)[0])
    pr_data.columns = cols
    
    # pr_data.loc[:, 'yr'] = pd.to_datetime(pr_data.loc[:,'datetime']).dt.year
    # pr_data = pr_data[pr_data['yr'].astype(str)==str(yr)]
    
    return(pr_data)

def existing_patients(yr, db_path):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()    
        ep_qry = c.execute(""" SELECT DISTINCT last_name, first_name, pv.patient_id, pv.datetime, patient_number || ' - ' || last_name || ', ' || first_name || ' - ' || pn.datetime AS lastfirst
                               FROM patient_vitals pv
                               LEFT JOIN(SELECT *
                                         FROM daily_patient_numbers) pn
                               ON pv.patient_id = pn.patient_id
                               WHERE CAST(year as NVARCHAR) = '""" + str(yr) + """'
                               ORDER BY pn.datetime desc""")
                          
        ep_data = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(ep_qry.description)[0])
        ep_data.columns = cols 
    except:
        print('issue with existing_patients')
    
    return(ep_data)

def existing_patient_vitals(yr, db_path, ep):
    
    try:
        all_ep = existing_patients(yr, db_path)
        all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
        
        pid = int(all_ep.loc[0, 'patient_id'])
    
        conn = sqlite3.connect(db_path)
        c = conn.cursor()    
        pv_qry = c.execute(""" SELECT *
                               FROM patient_vitals
                               WHERE CAST(year as NVARCHAR) = '""" + str(yr) + """' and CAST(patient_id AS INTEGER) = """ + str(pid) +""" 
                               ORDER BY datetime desc""")
                          
        pv_data = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pv_qry.description)[0])
        pv_data.columns = cols 
    except:
        pv_data = 'issue with existing_patient_vitals'
        print('issue with existing_patient_vitals')
    
    return(pv_data)

def exist_patient_procs_notes(yr, db_path, ep):
    try:
        all_ep = existing_patients(yr, db_path)
        all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
        
        pid = int(all_ep.loc[0, 'patient_id'])
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()    
        pn_qry = c.execute(""" SELECT *
                               FROM patient_procs_notes
                               WHERE CAST(patient_id AS INTEGER) = """ + str(pid))
                          
        pn_data = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pn_qry.description)[0])
        pn_data.columns = cols 
        
    except:
        print('no procedures or notes for ' + str(ep))

    return(pn_data)

def existing_patient_diagdrug(yr, db_path, ep):

    try:
        all_ep = existing_patients(yr, db_path)
        all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
        
        pid = int(all_ep.loc[0, 'patient_id'])
    
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        diag_drug_qry = c.execute("""SELECT diag.diagnosis, drg.drug_name AS drug
                                     FROM patient_diag_drug pdd
                                     LEFT JOIN(SELECT * FROM drug_index) drg
                                     ON pdd.drug_id = drg.id and CAST(pdd.year AS NVARCHAR)= CAST(drg.year AS NVARCHAR)
                                     LEFT JOIN(SELECT * FROM diagnosis_index) diag
                                     ON pdd.diagnosis_id = diag.id and CAST(pdd.year AS NVARCHAR) = CAST(diag.year AS NVARCHAR)
                                     WHERE CAST(pdd.year AS NVARCHAR) = '""" + str(yr) + """' and CAST(patient_id AS INT)  = """ + str(pid) )
        diag_drug = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(diag_drug_qry.description)[0])
        diag_drug.columns = cols 
    except:
        diag_drug = 'issue with existing_patient_diag_drug'
        print('issue with existing_patient_diag_drug')
    
    return(diag_drug)

def existing_patient_labs(yr, db_path, ep):
    
    try:
        all_ep = existing_patients(yr, db_path)
        all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
        
        pid = int(all_ep.loc[0, 'patient_id'])
    
        conn = sqlite3.connect(db_path)
        c = conn.cursor()    
        lab_qry = c.execute(""" SELECT lab_name, lr.lab_value
                                FROM patient_lab_results lr
                                LEFT JOIN(SELECT DISTINCT lab_id, lab_name 
                                          FROM lab_results_index) li
                                ON lr.lab_id = li.lab_id
                                WHERE CAST(patient_id AS INTEGER) = """ + str(pid))
                          
        lab_data = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(lab_qry.description)[0])
        lab_data.columns = cols 
    except:
        lab_data = 'issue with existing_patient_labs'
        print('issue with existing_patient_labs')
    
    return(lab_data)

def exist_patient_glasses(yr, db_path, ep):
    
    try:
        all_ep = existing_patients(yr, db_path)
        all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
        
        pid = int(all_ep.loc[0, 'patient_id'])
    
        conn = sqlite3.connect(db_path)
        c = conn.cursor()    
        gl_qry = c.execute(""" SELECT reading_glasses  
                                FROM patient_glasses
                                WHERE CAST(patient_id AS INTEGER) = """ + str(pid))
                          
        gl_data = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(gl_qry.description)[0])
        gl_data.columns = cols 
    except:
        gl_data = pd.DataFrame(['No Glasses'], columns=['reading_glasses'])
        print('issue with existing_patient_labs')
    
    return(gl_data)

def diagdrug_recordviewer(yr, db_path):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()    
    dd_qry = c.execute("""SELECT first_name, last_name, diagnosis, drug_name
                          FROM patient_diag_drug pdd
                          
                          LEFT JOIN(SELECT DISTINCT patient_id, first_name, last_name, year
                                    FROM patient_vitals) pv
                          ON CAST(pdd.patient_id AS INT) = CAST(pv.patient_id AS INT) and CAST(pdd.year AS NVARCHAR) = CAST(pv.year AS NVARCHAR)

                          LEFT JOIN(SELECT *
                                    FROM diagnosis_index) di
                          ON pdd.diagnosis_id = di.id and CAST(pdd.year AS NVARCHAR) = CAST(di.year AS NVARCHAR)
                          LEFT JOIN(SELECT *
                                    FROM drug_index) dri
                          ON pdd.drug_id = dri.id and CAST(pdd.year AS NVARCHAR) = CAST(dri.year AS NVARCHAR)
                          WHERE CAST(pdd.year AS NVARCHAR) = '""" + str(yr) + """'
                          ORDER BY CAST(pdd.patient_id AS INT), last_name, first_name""")
                      
    dd_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(dd_qry.description)[0])
    dd_data.columns = cols
    
    return (dd_data)

def pharm_recordviewer(yr, db_path):
    
    try:
        yr = str(yr)
    except:
        print('yr is already a string')
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    # db_path = r'./data/dr_patient_data_23.db'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor() 
    
    pharm_qry = c.execute("""SELECT drug_id, pr.year, drug_name, dosage, ordered, distributed
                             FROM pharmacy_record pr
                             LEFT JOIN(SELECT *
                                       FROM drug_index) dri
                             ON pr.drug_id = dri.id and CAST(pr.year AS NVARCHAR) = CAST(dri.year AS NVARCHAR)
                             WHERE CAST(pr.year AS NVARCHAR) = '""" + str(yr) + """'""")
    pharm_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pharm_qry.description)[0])
    pharm_data.columns = cols
    
    pharm_data_ret = pharm_data[['drug_id', 'year', 'drug_name', 'dosage', 'ordered', 'distributed']]
    
    return(pharm_data_ret)

def pharm_years(db_path):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
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

def pharm_update_staging(pr_edit, db_path):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    pr_edit = pd.DataFrame(pr_edit)
    pr_edit.loc[:,'stage_update'] = pd.to_datetime(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M')

    
    # try:
        
        # conn = sqlite3.connect(db_path)
        # c = conn.cursor() 
        # pharmstage_qry = c.execute("""SELECT *
        #                               FROM pharmacy_staging""")
        # pharmstage = pd.DataFrame(c.fetchall())
        # cols = list(pd.DataFrame(pharmstage_qry.description)[0])
        # pharmstage.columns = cols
        
    #     pharmstage.loc[:,'stage_update'] = pd.to_datetime(pharmstage.loc[:,'stage_update']).dt.strftime('%Y-%m-%d %H:%M')
        
    # except:
    #     pharmstage = pd.DataFrame(columns = ['drug_id','year','drug_name','dosage','ordered','distributed','stage_update'])
    
    # staging_update = pharmstage._append(pr_edit)
    # staging_update = staging_update.sort_values(by = ['drug_id','stage_update'], ascending=False)
    # staging_update = staging_update.drop_duplicates(subset = ['drug_id'], keep='first')
        
    conn = sqlite3.connect(db_path)
    pr_edit.to_sql('pharmacy_staging', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    
def pharm_stage_view(db_path):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    try:
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor() 
        pharmstage_qry = c.execute("""SELECT *
                                      FROM pharmacy_staging""")
        pharmstage = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pharmstage_qry.description)[0])
        pharmstage.columns = cols
        
        pharmstage = pharmstage.drop(columns = ['stage_update'])
    except Exception as e:
        print(e)
        pharmstage = pd.DataFrame()
        # print('no updates have been made to pharmacy staging table')
        
    return(pharmstage)

def add_new_pharm(yr, pharm_add, diaglist, db_path):
    
    print(str(diaglist))
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    ###################################################################################################
    #diagnosis to drug handling...could be tricky here
    
    #diaglist = list(["Asthma/COPD", "Bacterial Respiratory Infections", "Burn", "TEST", "TEST2"])
    diaglist = pd.DataFrame(diaglist).T
    diaglist.columns = ['diagnosis']
    diaglist = diaglist.reset_index()
    
    diaglist.loc[:,'drug_name'] = pharm_add.loc[0,'drug_name']
    diaglist.loc[:,'year'] = str(yr)
    diaglist = diaglist[['year', 'diagnosis', 'drug_name']]
        
    conn = sqlite3.connect(db_path)
    diaglist.to_sql('diag_drug_ref_stage', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    
    
    ###################################################################################################
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor() 
    lastid_qry = c.execute("""SELECT MAX(drug_id) as lastid
                              FROM pharmacy_staging""")
    lastid = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lastid_qry.description)[0])
    lastid.columns = cols
    
    nextid = int(lastid.loc[0,'lastid']) + 1 
    
    pharm_add.loc[:,'drug_id'] = nextid
    pharm_add.loc[:,'stage_update'] = pd.to_datetime(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M')
    pharm_add = pharm_add[['drug_id', 'year', 'drug_name', 'dosage', 'ordered', 'distributed', 'stage_update']]
    pharm_add.to_sql('pharmacy_staging', conn, if_exists='append', index=False)
    
def pharm_submit(yr, db_path):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    #################################################################################################
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor() 
        ddr_stage_qry = c.execute("""SELECT *
                                      FROM diag_drug_ref_stage""")
        ddr_stage = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(ddr_stage_qry.description)[0])
        ddr_stage.columns = cols
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        diag_qry = c.execute("""SELECT * 
                                FROM diagnosis_index
                                WHERE CAST(year AS NVARCHAR) = '""" + str(yr) + """'""")
        diagidx = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(diag_qry.description)[0])
        diagidx.columns = cols
        
        nextid = int(diagidx.loc[:,'id'].max()) + 1
        diaglist = ddr_stage[['diagnosis']].drop_duplicates()
        
        diag_ids = diaglist.merge(diagidx[['id', 'diagnosis']], how = 'left', on = 'diagnosis')
        newdiags = diag_ids[diag_ids['id'].isna()].reset_index(drop=True).reset_index()
        if len(newdiags) > 0:
            newdiags.loc[:, 'id'] = newdiags.loc[:, 'index'] + nextid
            newdiags.loc[:,'year'] = str(yr)
            newdiags = newdiags[['year', 'id', 'diagnosis']]
            diagidx = diagidx._append(newdiags)
        
        ddr_stage = ddr_stage.merge(diagidx[['diagnosis','id']], how = 'left', on = ['diagnosis'])
        ddr_stage = ddr_stage.rename(columns = {'id':'diag_id'})
    except:
        print('There were no new drugs added to the system')
        
    #################################################################################################

    #################################################################################################

    pharm = pd.DataFrame(pharm_stage_view(db_path))
    pharm.loc[:,'year'] = str(yr)
    
    pharmsub = pharm[['drug_id','year','ordered', 'distributed']].reset_index(drop = True)
    pharmsub = pharmsub[pharmsub['ordered'] != '0']
    pharmsub = pharmsub[pharmsub['ordered'] != 0]
    
    drug_index = pharm[pharm['ordered'] != '0']
    drug_index = drug_index[drug_index['ordered'] != 0]
    drug_index = pharm[['year', 'drug_id', 'drug_name', 'dosage']]
    drug_index = drug_index.rename(columns = {'drug_id':'id'})
    
    
    try:
        rem = pharm[(pharm['ordered'] == '0') | (pharm['ordered'] == 0)].reset_index(drop=True)
        
        for i in range(len(rem)):
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE
                          FROM diagnosis_drug_ref
                          WHERE CAST(year AS NVARCHAR) = '""" + str(yr) + """' and 
                                CAST(drug_id AS INTEGER) = """ + str(int(rem.loc[i,'drug_id'])))
            conn.commit()
            conn.close()
            
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE
                          FROM drug_index
                          WHERE CAST(year AS NVARCHAR) = '""" + str(yr) + """' and 
                                CAST(id AS INTEGER) = """ + str(int(rem.loc[i,'drug_id'])))
            conn.commit()
            conn.close()
        
    except:
        print('No drugs were removed from diagnosis_drug_ref')
    
    try:
        ddr_stage = ddr_stage.merge(drug_index[['drug_name', 'id']], how = 'inner', on = ['drug_name'])
        ddr_stage = ddr_stage[['year', 'diag_id', 'id']]
        ddr_stage = ddr_stage.rename(columns = {'id':'drug_id'})
    except:
        print('No new drugs added')
    
    currentyr = datetime.date.today().year
    
    yr = int(pharmsub.loc[0,'year'])
    if yr >= currentyr:
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE
                          FROM pharmacy_record
                          WHERE CAST(year AS NVARCHAR) = '""" + str(yr) + """'""")
            conn.commit()
            conn.close()
            
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE
                          FROM drug_index
                          WHERE CAST(year AS NVARCHAR) = '""" + str(yr) + """'""")
            conn.commit()
            conn.close()
            
            
            pharmsub.loc[:,'year'] = pharmsub.loc[:,'year'].astype(str)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            pharmsub.to_sql('pharmacy_record', conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
            
            conn = sqlite3.connect(db_path)
            drug_index.to_sql('drug_index', conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
            
            if 'ddr_stage' in locals():
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("""DELETE
                              FROM diagnosis_index
                              WHERE CAST(year AS NVARCHAR) = '""" + str(yr) + """'""")
                conn.commit()
                conn.close()
                
                conn = sqlite3.connect(db_path)
                diagidx.to_sql('diagnosis_index', conn, if_exists='append', index=False)
                conn.commit()
                conn.close()
    
                conn = sqlite3.connect(db_path)
                ddr_stage.to_sql('diagnosis_drug_ref', conn, if_exists='append', index=False)
                conn.commit()
                conn.close()
            
            res = 'Phamacy changes for ' + str(yr) + ' have been SUBMITTED!'
        
        except:
            res = 'error occurred on submit'
            print("error occurred")
    else:     
        res = 'You cannot edit a year in the past. ' + str(yr) + 'is not a current or future year. TRY AGAIN :)'
    
    
    return(res)
    
def patient_vitals_staging(first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight, db_path, userid):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_vitals_""" + userid)
        conn.commit()
        conn.close()
    except:
        print('temp vitals table did not exist')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE patient_vitals_""" + userid + """ (patient_id, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight, datetime, year)""")
    conn.commit()
    conn.close()
    
    pv_temp = pd.DataFrame([[0, first_name, last_name, age, sex, heart_rate, blood_pressure, resp_rate, O2_sat, weight,datetime.date.today(), datetime.date.today().year]],
                           columns = ['patient_id','first_name','last_name','age','sex', 'heart_rate', 'blood_pressure', 'resp_rate', 'O2_sat', 'weight','datetime', 'year'])

    conn = sqlite3.connect(db_path)
    pv_temp.to_sql('patient_vitals_' + userid, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    pv = c.execute("""SELECT * FROM patient_vitals_""" + userid)
    pv_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pv.description)[0])
    pv_return.columns = cols
    
    return(pv_return)


def diag_drug_staging(yr, diagnosis, drug, db_path, userid, create = 'Y'):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    # try:
    #     conn = sqlite3.connect(db_path)
    #     c = conn.cursor()
    #     c.execute("""DROP TABLE patient_diag_drug_temp""")
    #     conn.commit()
    #     conn.close()
    # except:
    #     print('temp patient_diag_drug table did not exist')
    if create == 'Y':
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""CREATE TABLE patient_diag_drug_""" + userid + """(year, patient_id, diagnosis_id, drug_id)""")
            conn.commit()
            conn.close()
        except: 
            print('temp patient_diag_drug table already exists')
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        di = c.execute("""SELECT id AS diagnosis_id, diagnosis 
                          FROM diagnosis_index 
                          WHERE diagnosis = '""" + str(diagnosis) + """' and 
                                CAST(year AS NVARCHAR) = '""" + str(yr) +"""'""")
        didata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(di.description)[0])
        didata.columns = cols
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        dri = c.execute("""SELECT id AS drug_id, drug_name 
                           FROM drug_index 
                           WHERE drug_name = '""" + str(drug) + """' and 
                                 CAST(year AS NVARCHAR) = '""" + str(yr) +"""'""")
        dridata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(dri.description)[0])
        dridata.columns = cols
        
        ddt = pd.DataFrame([[yr, 0, diagnosis, drug]], columns = ['year', 'patient_id', 'diagnosis', 'drug'])
        ddt = ddt.merge(didata, how = 'left', on = ['diagnosis'])
        ddt = ddt.merge(dridata, how = 'left', left_on = ['drug'], right_on = ['drug_name'])
        
        ddt_return = ddt[['diagnosis', 'drug']]
        ddt = ddt[['year','patient_id', 'diagnosis_id', 'drug_id']]
    
        conn = sqlite3.connect(db_path)
        ddt.to_sql('patient_diag_drug_' + userid, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()    
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    ddtc = c.execute("""SELECT diagnosis, drug_name AS drug
                        FROM patient_diag_drug_""" + userid + """ ddt
                        LEFT JOIN(SELECT *
                                  FROM diagnosis_index
                                  WHERE CAST(year AS NVARCHAR) = '""" + str(yr) +"""') di
                        ON ddt.diagnosis_id = di.id
                        LEFT JOIN(SELECT *
                                  FROM drug_index
                                  WHERE CAST(year AS NVARCHAR) = '""" + str(yr) +"""') dri
                        ON ddt.drug_id = dri.id""")
    ddt_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(ddtc.description)[0])
    ddt_return.columns = cols
    
    # ddt_return = pd.DataFrame([[diagnosis, drug, procs, notes]])
    
    return(ddt_return)

def diagdrug_staging_ep(yr, db_path, userid, ep):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_diag_drug_""" + userid)
        c.execute("""CREATE TABLE patient_diag_drug_""" + userid + """ (year, patient_id, diagnosis_id, drug_id)""")
        conn.commit()
        conn.close()
    except:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE patient_diag_drug_""" + userid + """ (year, patient_id, diagnosis_id, drug_id)""")
        conn.commit()
        conn.close()
        
    all_ep = existing_patients(yr, db_path)
    all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
    
    pid = int(all_ep.loc[0, 'patient_id'])
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    diag_drug_qry = c.execute("""SELECT pdd.year, pdd.patient_id, diag.id as diagnosis_id, drg.id as drug_id
                                 FROM patient_diag_drug pdd
                                 LEFT JOIN(SELECT * FROM drug_index) drg
                                 ON pdd.drug_id = drg.id and CAST(pdd.year AS NVARCHAR)= CAST(drg.year AS NVARCHAR)
                                 LEFT JOIN(SELECT * FROM diagnosis_index) diag
                                 ON pdd.diagnosis_id = diag.id and CAST(pdd.year AS NVARCHAR) = CAST(diag.year AS NVARCHAR)
                                 WHERE CAST(pdd.year AS NVARCHAR) = '""" + str(yr) + """' and CAST(patient_id AS INT)  = """ + str(pid) )
    diag_drug = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(diag_drug_qry.description)[0])
    diag_drug.columns = cols 
    
    conn = sqlite3.connect(db_path)
    diag_drug.to_sql('patient_diag_drug_' + userid, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()  

def daily_patient_numbers(yr, db_path, userid, ep):    
    
    all_ep = existing_patients(yr, db_path)
    all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
    
    pid = int(all_ep.loc[0, 'patient_id'])
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()    
    pn_qry = c.execute(""" SELECT *
                           FROM daily_patient_numbers
                           WHERE CAST(patient_id AS INTEGER) = """ + str(pid))
                      
    pn_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(pn_qry.description)[0])
    pn_data.columns = cols 
    
    pn = int(pn_data.loc[0,'patient_number'])
    
    return(pn_data)

def lab_staging_ep(yr, db_path, userid, ep):

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DROP TABLE patient_lab_results_""" + userid)
        c.execute("""CREATE TABLE patient_lab_results_""" + userid + """ (patient_id, lab_id, lab_value)""")
        conn.commit()
        conn.close()
    except:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""CREATE TABLE patient_lab_results_""" + userid + """ (patient_id, lab_id, lab_value)""")
        conn.commit()
        conn.close()

    all_ep = existing_patients(yr, db_path)
    all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
    
    pid = int(all_ep.loc[0, 'patient_id'])

    conn = sqlite3.connect(db_path)
    c = conn.cursor()    
    lr_qry = c.execute(""" SELECT *
                           FROM patient_lab_results
                           WHERE CAST(patient_id AS INTEGER) = """ + str(pid))
                      
    lrt_data = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lr_qry.description)[0])
    lrt_data.columns = cols 

    conn = sqlite3.connect(db_path)
    lrt_data.to_sql('patient_lab_results_' + userid, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()    

def lab_results_staging(lab_name, lab_value, db_path, userid, create = 'Y'):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    if create == "Y":
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""CREATE TABLE patient_lab_results_""" + userid + """ (patient_id, lab_id, lab_value)""")
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
        lrt.to_sql('patient_lab_results_' + userid, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()    
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lrtc = c.execute("""SELECT lab_name, lrt.lab_value
                        FROM patient_lab_results_""" + userid + """ lrt
                        LEFT JOIN(SELECT DISTINCT lab_id, lab_name
                                  FROM lab_results_index) lri
                        ON lrt.lab_id = lri.lab_id""")
    lrt_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lrtc.description)[0])
    lrt_return.columns = cols
        
    # ddt_return = pd.DataFrame([[diagnosis, drug, procs, notes]])
    
    return(lrt_return)

def selected_diagnosis(diagnosis, db_path, userid, read = 'Y', delete = 'N'):
    if read != 'Y':
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DROP TABLE selected_diagnosis_""" + userid)
            c.execute("""CREATE TABLE selected_diagnosis_""" + userid + """ (diagnosis)""")
            conn.commit()
            conn.close()
        except:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""CREATE TABLE selected_diagnosis_""" + userid + """ (diagnosis)""")
            conn.commit()
            conn.close()
            
            
        diagnosis = pd.DataFrame([diagnosis], columns = ['diagnosis'])    
        conn = sqlite3.connect(db_path)
        diagnosis.to_sql('selected_diagnosis_' + userid, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()  
        
    else:
        
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            diag_qry = c.execute("""SELECT diagnosis
                                  FROM selected_diagnosis_""" + userid )
            diagnosis = pd.DataFrame(c.fetchall())
            cols = list(pd.DataFrame(diag_qry.description)[0])
            diagnosis.columns = cols
        except:
            diagnosis = pd.DataFrame()
            
    if delete == 'Y':   
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DROP TABLE selected_diagnosis_""" + userid)
            conn.commit()
            conn.close()
        except:
            print('selected_diagnosis_ did not exist to delete')
            
    return(diagnosis)

def selected_lab(labname, db_path, userid, read = 'Y', delete = 'N'):
    if read != 'Y':
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DROP TABLE selected_lab_""" + userid)
            c.execute("""CREATE TABLE selected_lab_""" + userid + """ (lab_name)""")
            conn.commit()
            conn.close()
        except:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""CREATE TABLE selected_lab_""" + userid + """ (lab_name)""")
            conn.commit()
            conn.close()
            
            
        labname = pd.DataFrame([labname], columns = ['lab_name'])    
        conn = sqlite3.connect(db_path)
        labname.to_sql('selected_lab_' + userid, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()  
        
    else:
        
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            ln_qry = c.execute("""SELECT lab_name
                                  FROM selected_lab_""" + userid )
            labname = pd.DataFrame(c.fetchall())
            cols = list(pd.DataFrame(ln_qry.description)[0])
            labname.columns = cols
        except:
            labname = pd.DataFrame()
            
    if delete == 'Y':   
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DROP TABLE selected_lab_""" + userid)
            conn.commit()
            conn.close()
        except:
            print('selected_lab did not exist to delete')
            
    return(labname)

def diagdrug_staging_delete(diagnosis, db_path, userid):
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lrtc = c.execute("""SELECT diagnosis, diagnosis_id
                        FROM patient_diag_drug_""" + userid + """ lrt
                        LEFT JOIN(SELECT DISTINCT id, diagnosis
                                  FROM diagnosis_index) lri
                        ON lrt.diagnosis_id = lri.id""")
    lrt_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lrtc.description)[0])
    lrt_return.columns = cols
    
    lrt_return = lrt_return[['diagnosis_id']][lrt_return['diagnosis'] == diagnosis].reset_index(drop=True)
    lrt_return = int(lrt_return.loc[0,'diagnosis_id'])
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""DELETE 
                 FROM patient_diag_drug_""" + userid + """ 
                 WHERE CAST(diagnosis_id AS INTEGER) = """ + str(lrt_return))
    conn.commit()
    conn.close()
    

    
    print(diagnosis + ' was deleted for ' + userid)

        
def lab_results_staging_delete(labname, db_path, userid):
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lrtc = c.execute("""SELECT lab_name, lrt.lab_id
                        FROM patient_lab_results_""" + userid + """ lrt
                        LEFT JOIN(SELECT DISTINCT lab_id, lab_name
                                  FROM lab_results_index) lri
                        ON lrt.lab_id = lri.lab_id""")
    lrt_return = pd.DataFrame(c.fetchall())
    cols = list(pd.DataFrame(lrtc.description)[0])
    lrt_return.columns = cols
    
    lrt_return = lrt_return[['lab_id']][lrt_return['lab_name'] == labname].reset_index(drop=True)
    lrt_return = int(lrt_return.loc[0,'lab_id'])
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""DELETE 
                 FROM patient_lab_results_""" + userid + """ 
                 WHERE CAST(lab_id AS INTEGER) = """ + str(lrt_return))
    conn.commit()
    conn.close()
    

    
    print(labname + ' was deleted for ' + userid)

def final_submit(fname, lname, age, sex, weight, hr, bp, rr, o2sat, procs, notes, glasses, db_path, userid, yr, ep):
    
    # db_path = 'C:/Users/jaett/Documents/GitHub/scholarly/data/dr_patient_data_23.db'
    
    if ep != '':
        all_ep = existing_patients(yr, db_path)
        all_ep = all_ep[all_ep['lastfirst'] == ep].reset_index(drop = True)
        
        patient_id = int(all_ep.loc[0, 'patient_id'])
        
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""DELETE FROM patient_vitals WHERE CAST(patient_id AS INT) = """ + str(patient_id))
        conn.commit()
        conn.close()
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE FROM patient_lab_results WHERE CAST(patient_id AS INT) = """ + str(patient_id))
            conn.commit()
            conn.close()
        except: 
            print('patient_lab_results did not exist for patient ' + str(ep))
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE FROM patient_diag_drug WHERE CAST(patient_id AS INT) = """ + str(patient_id))
            conn.commit()
            conn.close()
        except: 
            print('patient_diag_drug did not exist for patient ' + str(ep))
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE FROM patient_procs_notes WHERE CAST(patient_id AS INT) = """ + str(patient_id))
            conn.commit()
            conn.close()
        except: 
            print('patient_procs_notes did not exist for patient ' + str(ep))            
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("""DELETE FROM patient_glasses WHERE CAST(patient_id AS INT) = """ + str(patient_id))
            conn.commit()
            conn.close()
        except: 
            print('patient_glasses did not exist for patient ' + str(ep))            
            
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        pn = c.execute("""SELECT patient_number
                          FROM daily_patient_numbers
                          WHERE CAST(patient_id AS INTEGER) = """ + str(patient_id))
        pndata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pn.description)[0])
        pndata.columns = cols
        
        pn = int(pndata.loc[0, 'patient_number'])
        
    else: 
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        pdd = c.execute('SELECT MAX(CAST(patient_id AS INT)) as last_id FROM patient_vitals')
        pdddata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pdd.description)[0])
        pdddata.columns = cols
        
        patient_id = int(pdddata.loc[0,'last_id']) + 1
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        pn = c.execute("""SELECT *
                          FROM daily_patient_numbers""")
        pndata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pn.description)[0])
        pndata.columns = cols

        pndata = pndata[['patient_number']][pd.to_datetime(pndata['datetime']) >= pd.to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))]
        # pndata = pndata[['patient_number']][pd.to_datetime(pndata['datetime']) >= pd.to_datetime('2025-04-22')]]]
        if len(pndata) > 0:
            pn = pndata.loc[:,'patient_number'].max() + 1
        else:
            pn = 1
        
        pndata = pd.DataFrame([[patient_id, pd.to_datetime(datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S'), pn]], columns = ['patient_id', 'datetime', 'patient_number'])
        
        conn = sqlite3.connect(db_path)
        pndata.to_sql('daily_patient_numbers', conn, if_exists='append', index=False)
        conn.commit()
        conn.close() 
    
    #patient vitals section-------------------------------------------------------------
    try:
        dt = pd.to_datetime('now').strftime("%Y-%m-%d %H:%M:%S")
        yr = datetime.date.today().year
        pv = pd.DataFrame([[patient_id, fname, lname, age, sex, hr, bp, rr, o2sat, weight, dt, yr]], 
                          columns = ['patient_id', 'first_name', 'last_name', 'age', 'sex', 'heart_rate', 'blood_pressure', 'resp_rate', 'O2_sat', 'weight','datetime', 'year'])
        
    
        conn = sqlite3.connect(db_path)
        pv.to_sql('patient_vitals', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()  
    except:
        print('no vitals entered yet')
    

    #patient lab results section--------------------------------------------------------
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        lrt = c.execute('SELECT * FROM patient_lab_results_' + userid)
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
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        pdd = c.execute('SELECT * FROM patient_diag_drug_' + userid)
        pdddata = pd.DataFrame(c.fetchall())
        cols = list(pd.DataFrame(pdd.description)[0])
        pdddata.columns = cols
        
        pdddata.loc[:,'patient_id'] = patient_id
        
        conn = sqlite3.connect(db_path)
        pdddata.to_sql('patient_diag_drug', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()    
    except:
        print('no diag_drugs entered yet')
    #patient procedures and notes section----------------------------------------------------
    try:
        ppn = pd.DataFrame([[patient_id, procs, notes]], columns = ['patient_id', 'procs', 'notes'])
        
        conn = sqlite3.connect(db_path)
        ppn.to_sql('patient_procs_notes', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()    
    except:
        print('no procs notes entered yet')
        
    #patient glasses section ----------------------------------------------------------------
    if glasses != 'No Glasses':
        glasses = pd.DataFrame([[patient_id, glasses]], columns = ['patient_id', 'reading_glasses'])
        
        conn = sqlite3.connect(db_path)
        glasses.to_sql('patient_glasses', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()

    success_text = str(pn)

    return(success_text)
    
    
    
    # DELETE FROM patient_vitals WHERE patient_id = 1
    # DELETE FROM patient_lab_results WHERE patient_id = 1
    # DELETE FROM patient_diag_drug WHERE patient_id = 1
    # DELETE FROM patient_procs_notes WHERE patient_id = 1
    # DELETE FROM patient_glasses WHERE patient_id = 1

    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_vitals WHERE CAST(patient_id AS INT)> 0""")
    # conn.commit()
    # conn.close()
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM daily_patient_numbers WHERE CAST(patient_id AS INT) > 0""")
    # conn.commit()
    # conn.close()   
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_lab_results WHERE CAST(patient_id AS INT) > 0""")
    # conn.commit()
    # conn.close()
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_diag_drug WHERE CAST(patient_id AS INT) > 0""")
    # conn.commit()
    # conn.close()  
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_procs_notes WHERE CAST(patient_id AS INT) > 0""")
    # conn.commit()
    # conn.close()      
    
    # conn = sqlite3.connect(db_path)
    # c = conn.cursor()
    # c.execute("""DELETE FROM patient_glasses WHERE CAST(patient_id AS INT) > 0""")
    # conn.commit()
    # conn.close()          
    