# DR Patient Med Recorder

library(shiny)
library(shinyjs)
library(bslib)
library(DT)
library(reticulate)
library(dplyr)
library(RSQLite)


# setwd("C:/Users/jaett/Documents/GitHub/scholarly")

# use_python("C:/Users/steve/anaconda3/python.exe")

use_python("C:\\Users\\jaett\\anaconda3\\python.exe")
dir <- paste0(getwd(), '/dr_patient_data_23.db')
diagdrug_pull <- import_from_path("dr_patient_modules",getwd())

#make this run every time app is refreshed
# cleartemps <- diagdrug_pull$cleartemps(db_path = dir)
#create a clear all staging tables module
clear_pharm <- diagdrug_pull$clear_pharm(db_path = dir)

#runApp("dr_patient_recorder.R")

ui <- fluidPage(
  useShinyjs(),
  
  conditionalPanel(condition = "input.enter_user_btn == 1 && input.userid.length > 0",
                   fluidRow(column(12,style='padding-top: 5px; margin-bottom:-50px;', uiOutput("currentuser_txt")))),
  
  fluidRow(column(12, uiOutput("titletext"))),
  fluidRow(),
  
  conditionalPanel(condition = "input.enter_user_btn == 0",
                   fluidRow(column(12, uiOutput('userid_txt'))),
                   fluidRow(column(2, style='padding-top:5px;', textInput('userid', 'UserId')),
                            column(1, style='padding-top:30px;', actionButton('enter_user_btn', 'ENTER', style="background-color: #0f6ff3; size: 10px; border-color: #2e6da4; font-weight: bold;"))),
  ),
  
  conditionalPanel(condition = "input.enter_user_btn == 1 && input.userid.length > 0",
  tabsetPanel(

    tabPanel('New Patient',
             fluidRow(column(3,uiOutput('br_text'))),
             fluidRow(column(1, actionButton("refresh_vitals_btn", "REFRESH", style="background-color: #0f6ff3; border-color: #2e6da4; font-weight: bold;"))),
             fluidRow(column(12,uiOutput("l1_txt"))),
             fluidRow(column(5, uiOutput("exist_patient_slt"))),
             fluidRow(column(12,uiOutput("vitals_txt"))),
             fluidRow(column(2, textInput("fname_input","First Name", "")), column(2, style='padding-left:0px;',textInput("lname_input","Last Name", ""))), 
             fluidRow(column(2, textInput("age_input","Age", "")), 
                      column(2, style='padding-left:0px;', uiOutput('slt_sex')), 
                      column(2, style='padding-left:0px;', textInput("wt_input","Weight", "")),
                      column(2, style='padding-left:0px;', textInput("hr_input","Heart Rate", "",))), 
             fluidRow(column(2, textInput("bp_input","Blood Pressure", "",)), 
                      column(2, style='padding-left:0px;', textInput("rr_input","Resp Rate", "",)),
                      column(2, style='padding-left:0px;', textInput("o2s_input","O2 Sat", "",))),
             # fluidRow(column(2, style='padding-top:20px;' ,actionButton("save_vitals_btn", "Save Vitals", style="background-color: gray; border-color: #2e6da4"))),
             # fluidRow(column(12,uiOutput('patient_vitals_temp'))),
             fluidRow(column(12,uiOutput("l2_txt"))),
             fluidRow(column(12,uiOutput("labres_txt1"))),
             fluidRow(column(3,uiOutput('slt_lab_name')), column(2, style='padding-left:0px;',uiOutput('slt_lab_val'))),
             fluidRow(column(2, style='padding-top:20px;' ,actionButton("add_lab_btn", "Add Lab", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(12, hidden(dataTableOutput('patient_lab_res_temp')))),
             fluidRow(column(12,uiOutput("l3_txt"))),
             fluidRow(column(12,uiOutput("diagdrug_txt1"))),
             fluidRow(column(12,uiOutput("diagdrug_txt2"))),
             
             fluidRow(column(2,uiOutput('slt_diag_np')), column(2, style='padding-left:0px;',uiOutput('slt_drug_np'))),
             fluidRow(column(2, style='padding-top:20px;' ,actionButton("save_diagdrug_btn", "Add Diagnosis", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(12,hidden(dataTableOutput('patient_diag_drug_temp')))),
             fluidRow(column(12,uiOutput("l4_txt"))),
             fluidRow(column(12,uiOutput("proc_note_txt"))),
             fluidRow(style = 'padding-left: 15px; padding-right: 15px;', textAreaInput("proc_txt","Procedures", "",'100%' ,'100px')),
             fluidRow(style = 'padding-left: 15px; padding-right: 15px;', textAreaInput("notes_txt","Notes", "",'100%' ,'100px')),
             fluidRow(column(12,uiOutput("l5_txt"))),
             fluidRow(column(12,uiOutput("glasses_txt"))),
             fluidRow(column(2,uiOutput('slt_glasses'))),
             fluidRow(column(12,uiOutput("l6_txt"))),
             fluidRow(column(2, style='padding-top:20px;' ,actionButton("submit_btn", "SUBMIT", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(3,uiOutput('final_submit'))),
             fluidRow(column(3,uiOutput('br_text2')))
             
             
             ),
    tabPanel('Record Viewer',
             fluidRow(column(10, offset = 1,style = 'padding-left: 0px;',uiOutput('patient_records_tbl'))),
             fluidRow(column(10, offset = 1,style = 'padding-left: 0px; padding-top: 50px;',uiOutput('diag_drug_tbl')))
             ),
    tabPanel('Pharmacy - Admin Only',
             # fluidRow(column(12,uiOutput("ws1"))),
             # fluidRow(column(2, style='padding-top:20px;' ,actionButton("edit_exist_pharm_btn", "Edit Existing Pharmacy", style="background-color: gray; border-color: #2e6da4"))),
             # fluidRow(column(2, style='padding-top:20px;' ,actionButton("create_new_pharm_btn", "Create New Pharmacy", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(2, style='padding-top:5px;', passwordInput('psswrd', 'Password')),
                      column(1, style='padding-top:30px;', actionButton('enter_pass_btn', 'ENTER', style="background-color: #4a90f1; size: 10px; border-color: #2e6da4"))),
             fluidRow(column(2, style='padding-top:20px;' ,hidden(actionButton("save_pharm_changes_btn", "Save Changes", style="background-color: gray; border-color: #2e6da4")))),
             fluidRow(column(2, style='padding-top:20px;', hidden(uiOutput('pharm_refyr_slt'))),
                      column(2, style='padding-top:20px;', hidden(uiOutput('pharm_newyr_slt'))),
                      column(2, style='padding-top:45px;', hidden(actionButton('sub_pharm_btn', 'SUBMIT', style="background-color: #4a90f1; size: 10px; border-color: #2e6da4")))),
             fluidRow(column(12,uiOutput("ws2"))),
             fluidRow(column(10, offset = 1, hidden(uiOutput('pharm_note_txt')))),
             fluidRow(column(2, offset = 1, hidden(actionButton("create_new_drug_btn", "Add New Drug", style="background-color: green; size: 10px; border-color: #2e6da4")))),
             fluidRow(column(10, offset = 1, dataTableOutput('pharm_ref_tbl')))
             )
  )
  )
)
server <- function(input, output, session) {
  
  # load("working_dataset.RData")
  
  
  output$titletext <- renderUI({HTML(paste('<p style="font-size:25px;"><br><b>DR Patient Medical Recorder/Viewer Tool<b></p><br>'))})
  
  output$userid_txt <- renderUI({HTML(paste('<p style="font-size:15px;color: red"><b>***Please enter your name for record keeping.<b></p><br>'))})
  output$currentuser_txt <- renderUI({HTML(paste('<p style="font-size:10px;color: #0f6ff3"><b>Current User: ',toString(input$userid),'<b></p><br>'))})
  
  output$vitals_txt <- renderUI({HTML(paste('<p style="font-size:15px;background-color: #FFFF00;"><b>Patient Vitals<b></p><br>'))})
  output$l1_txt <- renderUI({HTML(paste('<p style="font-size:15px; margin-bottom: -10px;">________________________________________________________________________________________________________</p><br>'))})
  output$l2_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  output$labres_txt1 <- renderUI({HTML(paste('<p style="font-size:15px; background-color: #FFFF00;"><b>Lab Tests and Results</b></p>'))})
  output$l3_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  output$diagdrug_txt1 <- renderUI({HTML(paste('<p style="font-size:15px;background-color: #FFFF00;"><b>Enter Diagnosis and Select Corresponding Drug</b></p>'))})
  output$diagdrug_txt2 <- renderUI({HTML(paste('<p style="font-size:12px;">NOTE: you may submit as many diagnoses as needed per patient<b></p><br>'))})
  output$l4_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  output$proc_note_txt <- renderUI({HTML(paste('<p style="font-size:15px;background-color: #FFFF00;"><b>Procedures & Notes<b></p><br>'))})
  output$l5_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  output$glasses_txt <- renderUI({HTML(paste('<p style="font-size:15px;background-color: #FFFF00;"><b>Glasses<b></p><br>'))})
  output$l6_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  
  output$pharm_note_txt <- renderUI({HTML(paste('<p style="font-size: 10px; color: red;"><b>***Pharmacy Tabble is editable.  Double click on any value to edit. You can edit the current year or create a new year based on previous year data.<b></p><br>'))})
  output$ws1 <- renderUI({HTML(paste0('<br><br>'))})
  output$ws2 <- renderUI({HTML(paste0('<br><br>'))})
  
  dir <- paste0(getwd(), '/dr_patient_data_23.db')
  
  observeEvent(input$enter_user_btn, {
    
    if (trimws(toString(input$userid)) == '') {
      
      showModal(modalDialog(
        title = "Bad User Id Entry",
        paste0("Please do not submit an empty userid.  Try Again :)!"),
        
        footer = fluidRow(column(1, style='padding-left:75px;', actionButton("baduserid_btn", "OK")))
      ))
      
    }
    
  })
  
  observeEvent(input$baduserid_btn,{
    
    session$reload()
    
    })
  
  observeEvent(c(input$refresh_vitals_btn, input$enter_user_btn), {
    
                                          cleartemps <- diagdrug_pull$cleartemps(db_path = dir, userid = toString(input$userid))
                                          
                                          existing_patients <- diagdrug_pull$existing_patients(substr(Sys.Date(), 1, 4), db_path = dir)
                                          ep_choices <- existing_patients$lastfirst
                                          updateSelectInput(session, "exist_patient_slt","Edit Existing Patient",choices = c("", ep_choices))
                                          
                                          updateTextInput(session, "fname_input", value = "")
                                          updateTextInput(session, "lname_input", value = "")
                                          updateTextInput(session, "age_input", value = "")
                                          updateTextInput(session, "sex_input", value = "")
                                          updateTextInput(session, "wt_input", value = "")
                                          updateTextInput(session, "hr_input", value = "")
                                          updateTextInput(session, "bp_input", value = "")
                                          updateTextInput(session, "rr_input", value = "")
                                          updateTextInput(session, "o2s_input", value = "")
                                          
                                          lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
                                          lab_names <- unique(lab_test_ref$lab_name)
                                          updateSelectInput(session, "slt_lab_name", label = "Select Lab Test", choices = c("No Labs",lab_names))
                                          
                                          diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
                                          diagnosis_choices <- diagnosis_drug_ref$diagnosis
                                          updateSelectInput(session, "slt_diag_np", label = "Select Diagnosis", choices = c("No Diagnosis", diagnosis_choices))
                                          
                                          
                                          updateTextAreaInput(session, "proc_txt", value = "")
                                          updateTextAreaInput(session, "notes_txt", value = "")
                                          
                                          updateSelectInput(session, "slt_glasses", label = "Select Glassess", choices = c("No Glasses","1.00","1.25","1.5","1.75","2.00","2.25","2.5","2.75","3.00","3.25","3.5","3.75","4.00"))
                                          
                                          shinyjs::hide("patient_diag_drug_temp")
                                          shinyjs::hide("patient_lab_res_temp")
                                          
                                          })
  
  
  output$exist_patient_slt <- renderUI({ 
    
              existing_patients <- diagdrug_pull$existing_patients(substr(Sys.Date(), 1, 4), db_path = dir)
              ep_choices <- existing_patients$lastfirst


              selectInput("exist_patient_slt",
                          "Edit Existing Patient",
                          choices = c("", ep_choices))
    
    })
  
  observeEvent(input$exist_patient_slt, {
    #blah, test2 - 2025-04-17 16:14:16
    if (toString(input$exist_patient_slt) != '') {
              epv <- diagdrug_pull$existing_patient_vitals(substr(Sys.Date(), 1, 4), dir, toString(input$exist_patient_slt))
              ep_pn <- diagdrug_pull$exist_patient_procs_notes(substr(Sys.Date(), 1, 4), dir, toString(input$exist_patient_slt))
              ep_glasses <- diagdrug_pull$exist_patient_glasses(substr(Sys.Date(), 1, 4), dir, toString(input$exist_patient_slt))
              
              # fn <- toString(epv$first_name[1])
              try({
              updateTextInput(session, "fname_input", value = toString(epv$first_name[1]))
              updateTextInput(session, "lname_input", value = toString(epv$last_name[1]))
              updateTextInput(session, "age_input", value = toString(epv$age[1]))
              updateTextInput(session, "sex_input", value = toString(epv$sex[1]))
              updateTextInput(session, "wt_input", value = toString(epv$weight[1]))
              updateTextInput(session, "hr_input", value = toString(epv$heart_rate[1]))
              updateTextInput(session, "bp_input", value = toString(epv$blood_pressure[1]))
              updateTextInput(session, "rr_input", value = toString(epv$resp_rate[1]))
              updateTextInput(session, "o2s_input", value = toString(epv$O2_sat[1]))
              
              updateTextAreaInput(session, "proc_txt", value = toString(ep_pn$procs[1]))
              updateTextAreaInput(session, "notes_txt", value = toString(ep_pn$notes[1]))
              
              updateTextInput(session, "slt_glasses", value = toString(ep_glasses$reading_glasses[1]))
              
              })
    }
    
  })
  
  observeEvent(c(input$save_diagdrug_btn, input$exist_patient_slt, input$deletediag_btn), {
                                    ln <- diagdrug_pull$selected_diagnosis(diagnosis = ' ', db_path = dir, userid = toString(input$userid), read = 'Y', delete = 'N')
                                    pddemp <- data.frame()
                                    
                              tryCatch(
                                expr = {
                                    tryCatch(
                                      
                                      expr = {
                                        
                                        if((toString(input$slt_diag_np) != 'No Diagnosis') && (toString(input$userid) != '')) {
                                          
                                          pddemp <- diagdrug_pull$diag_drug_staging(substr(Sys.Date(), 1, 4), toString(input$slt_diag_np),toString(input$slt_drug_np), db_path = dir, userid = toString(input$userid), create = 'Y')
                                          pddemp <- pddemp[c("diagnosis","drug")]
                                          
                                        } else if ((toString(input$exist_patient_slt) == '') && (toString(input$userid) != '')) {
                                          
                                          pddemp <- diagdrug_pull$diag_drug_staging(substr(Sys.Date(), 1, 4), toString(' '),toString(' '), db_path = dir, userid = toString(input$userid), create = 'N')
                                          pddemp <- pddemp[c("diagnosis","drug")]
                                          
                                        } else if ((toString(input$exist_patient_slt) != '') && (length(ln) == 0)) {
                                          
                                          pddemp <- diagdrug_pull$diagdrug_staging_ep(substr(Sys.Date(), 1, 4), db_path = dir, userid = toString(input$userid), ep = toString(input$exist_patient_slt))
                                          print('updated diagdrug staging from existing patient')
                                          pddemp <- diagdrug_pull$existing_patient_diagdrug(substr(Sys.Date(), 1, 4), db_path = dir, ep = toString(input$exist_patient_slt))
                                          print('pulled existing patient diag drug work')
                                          
                                        } else if (length(ln) > 0) {
                                          pddemp <- diagdrug_pull$diag_drug_staging(substr(Sys.Date(), 1, 4), toString(' '),toString(' '), db_path = dir, userid = toString(input$userid), create = 'N')
                                          pddemp <- pddemp[c("diagnosis","drug")]
                                          print('pulled staging')
                                          
                                        }
                                        
                                      },
                                      error = function(e){
                                        print('nothing needed to run | diag drug')
                                      })


                                        output$patient_diag_drug_temp <- DT::renderDataTable(pddemp, rownames = FALSE, selection = 'single', options = list(dom = 't')) 
                                        shinyjs::show("patient_diag_drug_temp")
                                        
                                        if (input$slt_diag_np != "No Diagnosis") {
                                          diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
                                          diagnosis_choices <- diagnosis_drug_ref$diagnosis
                                          updateSelectInput(session, "slt_diag_np", label = "Select Diagnosis", choices = c("No Diagnosis", diagnosis_choices))
                                        }
                                        
                                      
                                      },
                                      error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))}
                                    )
                                    
                                    


                                  })
  
  observeEvent(input$patient_diag_drug_temp_cell_clicked, {
    
    if(length(input$patient_diag_drug_temp_cell_clicked) > 0) {

      #get values
      info <- input$patient_diag_drug_temp_cell_clicked
      i = as.numeric(info$row)
      
      print(paste0('clicked lab table on ', toString(info)))
      
      # pddtemp <- diagdrug_pull$lab_results_staging(toString(' '),toString(' '), db_path = dir, userid = toString(input$userid), create = 'N')
      pddtemp <- diagdrug_pull$diag_drug_staging(substr(Sys.Date(), 1, 4), toString(' '),toString(' '), db_path = dir, userid = toString(input$userid), create = 'N')
      pddtemp <- pddtemp[c("diagnosis","drug")]
      pddtemp <- toString(pddtemp$diagnosis[i])
      print(pddtemp)
      
      slt_diag <- diagdrug_pull$selected_diagnosis(diagnosis = pddtemp, db_path = dir, userid = toString(input$userid), read = 'N', delete = 'N')
      
      
      showModal(modalDialog(
        title = "Delete Diagnosis???",
        pddtemp,
        footer = fluidRow(column(1, actionButton("deletediag_btn", "DELETE")), column(1, style='padding-left:75px;', modalButton("CANCEL"))
        )
      ))
      
      
    }
  })
  
  observeEvent(input$deletediag_btn, {
    
    
    print('about to call delete operation...')
    ln <- diagdrug_pull$selected_diagnosis(diagnosis = ' ', db_path = dir, userid = toString(input$userid), read = 'Y', delete = 'N')
    ln <- toString(ln$diagnosis[1])
    print(ln)
    if (ln != '') {
      print(ln)
      diagdrug_pull$diagdrug_staging_delete(diagnosis = ln,db_path = dir, userid = toString(input$userid))
      print('deleted')
      removeModal()
    }
    
    # delay(1000, print("delay 1 second"))
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
    diagnosis_choices <- diagnosis_drug_ref$diagnosis
    updateSelectInput(session, "slt_diag_np", label = "Select Diagnosis", choices = c("No Diagnosis", diagnosis_choices))
    
  })
  

  
  observeEvent(c(input$add_lab_btn, input$exist_patient_slt, input$deletelab_btn), { 
                                    plrtemp <- data.frame()
                                    ln <- diagdrug_pull$selected_lab(labname = ' ', db_path = dir, userid = toString(input$userid), read = 'Y', delete = 'N')
                                    
                                    tryCatch(

                                      expr = { 
                                                tryCatch({
                                                   if ((toString(input$slt_lab_name) != 'No Labs')  && (toString(input$userid) != '')){
                                                       plrtemp <- diagdrug_pull$lab_results_staging(isolate(input$slt_lab_name),isolate(input$slt_lab_val), db_path = dir, userid = toString(input$userid), create = 'Y')
                                                       plrtemp <- plrtemp[c("lab_name","lab_value")]
                                                     
                                                   } else if ((toString(input$exist_patient_slt) == '') && (toString(input$userid) != '')) {
                                                   
                                                       plrtemp <- diagdrug_pull$lab_results_staging(' ', ' ', db_path = dir, userid = toString(input$userid), create = 'N')
                                                       plrtemp <- plrtemp[c("lab_name","lab_value")]
                                                       
                                                       } else if ((toString(input$exist_patient_slt) != '') && (length(ln) == 0)){
                                                         plrtemp <- diagdrug_pull$lab_staging_ep(substr(Sys.Date(), 1, 4), db_path = dir, userid = toString(input$userid), ep = toString(input$exist_patient_slt))
                                                         print('updated lab staging from existing patient')
                                                         #pulls the same data to show in the interface
                                                         plrtemp <- diagdrug_pull$existing_patient_labs(substr(Sys.Date(), 1, 4), db_path = dir, ep = toString(input$exist_patient_slt))
                                                         print('pulled existing patient lab work')
                                                       } else if ((length(ln) > 0)){ #(toString(input$exist_patient_slt) != '') && 
                                                         
                                                         
                                                         plrtemp <- diagdrug_pull$lab_results_staging(' ', ' ', db_path = dir, userid = toString(input$userid), create = 'N')
                                                         plrtemp <- plrtemp[c("lab_name","lab_value")]
                                                         print('pulled staging')
                                                         
                                                         
                                                       }
                                                       
                                                 },
                                                          error = function(e){
                                                            
                                                            print('nothing needed to run')
                                                            
                                                         })
                                        
                              
                                                  
                                                  output$patient_lab_res_temp <- DT::renderDataTable(plrtemp, rownames = FALSE, selection = 'single', options = list(dom = 't')) #
                                                  shinyjs::show("patient_lab_res_temp")
                                                  
                                                  if (input$slt_lab_name != 'No Labs') {
                                                    lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
                                                    lab_names <- unique(lab_test_ref$lab_name)
                                                    updateSelectInput(session, "slt_lab_name", label = "Select Lab Test", choices = c("No Labs",lab_names))
                                                    
                                                    lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
                                                    lab_vals <- rbind(lab_test_ref$lab_value[lab_test_ref$lab_name==input$slt_lab_name])
                                                    updateSelectInput(session, "slt_lab_val", "Select Lab Result", choices = c(" ", lab_vals))
                                                  }
                                                  
                                      },
                                      error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))
                                        print(paste0('there was an error pulling labs for: ',toString(input$exist_patient_slt)))
                                        
                                  }
                                    )
  })
  
  observeEvent(input$patient_lab_res_temp_cell_clicked, {

    if(length(input$patient_lab_res_temp_cell_clicked) > 0) {
    # pr_edit <- diagdrug_pull$pharm_stage_view(db_path = dir)
    # if(length(pr_edit) == 0){pr_edit <- diagdrug_pull$pharm_recordviewer(toString(input$pharm_refyr_slt), db_path = dir)}
    
    
    # pr_edit[order(pr_edit$drug_name), ]
    
    #get values
    info <- input$patient_lab_res_temp_cell_clicked
    i = as.numeric(info$row)

    print(paste0('clicked lab table on ', toString(info)))

    plrtemp <- diagdrug_pull$lab_results_staging(toString(' '),toString(' '), db_path = dir, userid = toString(input$userid), create = 'N')
    plrtemp <- plrtemp[c("lab_name","lab_value")]
    plrtemp <- toString(plrtemp$lab_name[i])
    print(plrtemp)
    
    slt_lab <- diagdrug_pull$selected_lab(labname = plrtemp, db_path = dir, userid = toString(input$userid), read = 'N', delete = 'N')
    
    showModal(modalDialog(
      title = "Delete Lab???",
      plrtemp,
      footer = fluidRow(column(1,offset = 4, style='padding-left:75px;', actionButton("deletelab_btn", "DELETE"))
                        ,
                        column(1, offset=7, modalButton("CANCEL"))
                        )
    ))
    
    
    }
})
  
 observeEvent(input$deletelab_btn, {

   #creation of this button is triggering this action but the actual click isn't running this event : (

    print('about to call delete operation...')
    ln <- diagdrug_pull$selected_lab(labname = ' ', db_path = dir, userid = toString(input$userid), read = 'Y', delete = 'N')
    ln <- toString(ln$lab_name[1])
    print(ln)
    if (ln != '') {
      print(ln)
      diagdrug_pull$lab_results_staging_delete(labname = ln,db_path = dir, userid = toString(input$userid))
      print('deleted')
      removeModal()
      # ln <- diagdrug_pull$selected_lab(labname = ' ', db_path = dir, userid = toString(input$userid), read = 'Y', delete = 'Y')
    }

    # delay(1000, print("delay 1 second"))

    lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
    lab_names <- unique(lab_test_ref$lab_name)
    updateSelectInput(session, "slt_lab_name", label = "Select Lab Test", choices = c("No Labs",lab_names))

    lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
    lab_vals <- rbind(lab_test_ref$lab_value[lab_test_ref$lab_name==input$slt_lab_name])
    updateSelectInput(session, "slt_lab_val", "Select Lab Result", choices = c(" ", lab_vals))

 })
  
  observeEvent(input$submit_btn, {
                                  pn <- diagdrug_pull$final_submit(isolate(input$fname_input), isolate(input$lname_input), isolate(input$age_input), isolate(input$sex_input), 
                                                             isolate(input$wt_input), isolate(input$hr_input), isolate(input$bp_input), isolate(input$rr_input), isolate(input$o2s_input),
                                                             isolate(input$proc_txt), isolate(input$notes_txt), isolate(input$slt_glasses), 
                                                             db_path = dir, userid = toString(input$userid),
                                                             yr = substr(Sys.Date(), 1, 4), ep = toString(input$exist_patient_slt))
                                  
                                  existing_patients <- diagdrug_pull$existing_patients(substr(Sys.Date(), 1, 4), db_path = dir)
                                  ep_choices <- existing_patients$lastfirst
                                  updateSelectInput(session, "exist_patient_slt","Edit Existing Patient",choices = c("", ep_choices))
    
                                  updateTextInput(session, "fname_input", value = "")
                                  updateTextInput(session, "lname_input", value = "")
                                  updateTextInput(session, "age_input", value = "")
                                  updateTextInput(session, "sex_input", value = "")
                                  updateTextInput(session, "wt_input", value = "")
                                  updateTextInput(session, "hr_input", value = "")
                                  updateTextInput(session, "bp_input", value = "")
                                  updateTextInput(session, "rr_input", value = "")
                                  updateTextInput(session, "o2s_input", value = "")
                                  
                                  lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
                                  lab_names <- unique(lab_test_ref$lab_name)
                                  updateSelectInput(session, "slt_lab_name", label = "Select Lab Test", choices = c("No Labs",lab_names))
                                  
                                  
                                  diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
                                  diagnosis_choices <- diagnosis_drug_ref$diagnosis
                                  updateSelectInput(session, "slt_diag_np", label = "Select Diagnosis", choices = c("No Diagnosis", diagnosis_choices))
                                  
                                  
                                  updateTextAreaInput(session, "proc_txt", value = "")
                                  updateTextAreaInput(session, "notes_txt", value = "")
                                  
                                  updateSelectInput(session, "slt_glasses", label = "Select Glassess", choices = c("No Glasses","1.00","1.25","1.5","1.75","2.00","2.25","2.5","2.75","3.00","3.25","3.5","3.75","4.00"))
                                  
                                  cleartemps <- diagdrug_pull$cleartemps(db_path = dir, userid = toString(input$userid))
                                  
                                  shinyjs::hide("patient_diag_drug_temp")
                                  shinyjs::hide("patient_lab_res_temp")
                                  
                                  # diagdrug_pull$patient_number_assignment(db_path)
                                  
                                  showModal(modalDialog(
                                    title = "Success!",
                                    HTML(paste0('<p style="font-size:45px;"><b>#',pn,'<b></p>')),
                                    paste0('Patient submitted to the system successfully'),
                                    
                                    footer = fluidRow(column(1, style='padding-left:75px;', modalButton("OK")))
                                  ))
                                  
    
  })
  



  output$diag_drug_ref_tbl <- renderUI({
      ddr <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
      ddr <- ddr[c("diagnosis","drug_name","dosage","distribution")]
    
      DT::renderDataTable(ddr, rownames = FALSE,
                               options = list(autoWidth = TRUE,
                                              pageLength = 100))  
  })

  
  output$patient_records_tbl <- renderUI({
    pr <- diagdrug_pull$patientrecord_pull(substr(Sys.Date(), 1, 4), db_path = dir)
    # pr <- pr[c("diagnosis","drug_name","dosage","distribution")]
    
    DT::renderDataTable(pr, rownames = FALSE,
                        options = list(autoWidth = TRUE,
                                       pageLength = 100))  
  })
  
  output$diag_drug_tbl <- renderUI({
    
    dd <- diagdrug_pull$diagdrug_recordviewer(substr(Sys.Date(), 1, 4), db_path = dir)
    # pr <- pr[c("diagnosis","drug_name","dosage","distribution")]
    
    DT::renderDataTable(dd, rownames = FALSE,
                        options = list(autoWidth = TRUE,
                                       pageLength = 100))  
  })
  
  
  output$br_text <- renderUI({HTML(paste('<br>'))})
  output$br_text2 <- renderUI({HTML(paste('<br><br><br><br>'))})
  
  output$slt_sex <- renderUI({
    
    selectInput("sex_input", 
                "Sex", 
                choices = c(" ", "M","F"))
    
  })
  
    output$slt_diag_np <- renderUI({
    
                                    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
                                    diagnosis_choices <- diagnosis_drug_ref$diagnosis
                                    
                                    
                                    selectInput("slt_diag_np", 
                                                "Select Diagnosis", 
                                              choices = c("No Diagnosis", diagnosis_choices))
                                  
                                })
  
  output$slt_drug_np <- renderUI({
    
                                  diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
                                  meds <- rbind(diagnosis_drug_ref$drug_name[diagnosis_drug_ref$diagnosis==input$slt_diag_np])
                                  
                                  selectInput("slt_drug_np", 
                                              "Select Drug", 
                                              choices = meds)
                                })
  
  
  output$slt_lab_name <- renderUI({
    
                                    lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
                                    lab_names <- unique(lab_test_ref$lab_name)
                                    
                                    
                                    selectInput("slt_lab_name", 
                                                "Select Lab Test", 
                                                choices = c("No Labs",lab_names))
                                    
                                  })

  
  output$slt_lab_val <- renderUI({
    
                                  lab_test_ref <- diagdrug_pull$lab_tests_pull(db_path = dir)
                                  lab_vals <- rbind(lab_test_ref$lab_value[lab_test_ref$lab_name==input$slt_lab_name])
                                  
                                  
                                  selectInput("slt_lab_val", 
                                              "Select Lab Result", 
                                              choices = c(" ", lab_vals))
                                  
                                })
  
  output$slt_glasses <- renderUI({
    
                                  selectInput("slt_glasses", 
                                              "Select Glasses", 
                                              choices = c("No Glasses","1.00","1.25","1.5","1.75","2.00","2.25","2.5","2.75","3.00","3.25","3.5","3.75","4.00"))
                                  
                                })
  
  

  
  observeEvent(c(input$pharm_refyr_slt, input$pharm_newyr_slt, input$add_drug_btn, input$sub_pharm_btn),{
                
                output$pharm_ref_tbl <- renderDT({
                                                  pr <- data.frame()
                                                  tryCatch(                                
                  
                                                  {pr <- diagdrug_pull$pharm_stage_view(db_path = dir)
                                                   pr[order(pr$drug_name), ]
                                                  
                                                   if(input$pharm_newyr_slt != ''){pr$year <- toString(input$pharm_newyr_slt)
                                                                                   diagdrug_pull$pharm_update_staging(pr, db_path = dir)
                                                                                   
                                                  
                                                   DT::datatable(pr,
                                                                 rownames = FALSE,
                                                                 editable = TRUE,
                                                                 options = list(autoWidth = TRUE,
                                                                                pageLength = 100,
                                                                                dom = 't'))
                                                   } else {
                                                     
                                                     pr <- diagdrug_pull$pharm_recordviewer(yr, db_path = dir)
                                                     pr[order(pr$drug_name), ]
                                                    
                                                     DT::datatable(pr,
                                                                   rownames = FALSE,
                                                                   editable = TRUE,
                                                                   options = list(autoWidth = TRUE,
                                                                                  pageLength = 100,
                                                                                  dom = 't')) 
                                                   }
                                                  },
                                                  #if an error occurs, tell me the error
                                                  error=function(e) {
                                                    message('An Error Occurred in pharm admin tab...')
                                                    
                                                    if ((toString(input$pharm_newyr_slt) == '') & (toString(input$pharm_refyr_slt) == '')){
                                                      
                                                      print("No selections made in pharmacy admin tab yet...")
                                                      
                                                    } else {
                                                    
                                                    if(toString(input$pharm_newyr_slt) == '') {yr <- toString(input$pharm_refyr_slt)
                                                    } else {yr <- toString(input$pharm_newyr_slt)}
                                                    
                                                    pr <- diagdrug_pull$pharm_recordviewer(yr, db_path = dir)
                                                    pr[order(pr$drug_name), ]
                                                    # pr <- pr[c("diagnosis","drug_name","dosage","distribution")]
                                                    
                                                    if(input$pharm_newyr_slt != ''){pr$year <- toString(input$pharm_newyr_slt)}
                                                    
                                                    DT::datatable(pr,
                                                                  rownames = FALSE,
                                                                  editable = TRUE,
                                                                  options = list(autoWidth = TRUE,
                                                                                 pageLength = 100,
                                                                                 dom = 't'))
                                                    }
                                                  },
                                                  #if a warning occurs, tell me the warning
                                                  warning=function(w) {
                                                    message('A Warning Occurred')
                                                    print(w)
                                                    return(NA)
                                                  })
                })
  
  })

  
  observeEvent(input$pharm_newyr_slt, {
    if(input$pharm_newyr_slt != ''){
                      pr_edit <- diagdrug_pull$pharm_stage_view(db_path = dir)
                      if(length(pr_edit) == 0){pr_edit <- diagdrug_pull$pharm_recordviewer(toString(input$pharm_refyr_slt), db_path = dir)}
                      pr_edit$year <- toString(input$pharm_newyr_slt)
                      diagdrug_pull$pharm_update_staging(pr_edit, db_path = dir)}
    
    })
  
  
    observeEvent(input$pharm_refyr_slt, {
    if (toString(input$pharm_refyr_slt) != '') {
      shinyjs::show("pharm_ref_tbl")
      shinyjs::show("pharm_newyr_slt")
      shinyjs::show("create_new_drug_btn")
      shinyjs::show("pharm_note_txt")
      shinyjs::show("sub_pharm_btn")
    }
    
    
    })
    
    observeEvent(input$enter_pass_btn,{
      
      if (toString(input$psswrd) == 'blevins'){
        shinyjs::hide("psswrd")
        shinyjs::hide("enter_pass_btn")
        shinyjs::show("pharm_refyr_slt")
      } else {
        
        showModal(modalDialog(
          title = "Password Incorrect!",
          paste0("Password is incorrect.  Try Again! "),
          
          footer = fluidRow(column(1, style='padding-left:75px;', modalButton("OK")))
        ))
      }
    })

  
  
  output$pharm_refyr_slt <- renderUI({
    
    # pharm_yr <- diagdrug_pull$pharm_recordviewer()
    # pharm_yr <- as.list(unique(pharm_yr$year))
    
    pharm_yr <- as.list(diagdrug_pull$pharm_years(db_path = dir))
    
    
    selectInput("pharm_refyr_slt", 
                "Select Pharmacy Reference Year", 
                choices = c("",pharm_yr), 
                selected = substr(Sys.Date(), 1, 4))
    
  })
  
  output$pharm_newyr_slt <- renderUI({
    
    
    selectInput("pharm_newyr_slt", 
                "Select New Pharmacy Year", 
                choices = c("","2025","2026","2027", "2028","2029","2030"),
                selected = substr(Sys.Date(), 1, 4)
                )
    
  })
  

  observeEvent(input$pharm_ref_tbl_cell_edit, {
    
    pr_edit <- diagdrug_pull$pharm_stage_view(db_path = dir)
    if(length(pr_edit) == 0){pr_edit <- diagdrug_pull$pharm_recordviewer(toString(input$pharm_refyr_slt), db_path = dir)}
             
    
    # pr_edit[order(pr_edit$drug_name), ]

    #get values
    info = input$pharm_ref_tbl_cell_edit
    i = as.numeric(info$row)
    j = as.numeric(info$col) + 1
    k = toString(info$value)


    #write values to reactive
    if (j != 1){
                  pr_edit[i,j] <- k
                  pr_edit$year <- toString(input$pharm_newyr_slt)
                  
                  diagdrug_pull$pharm_update_staging(pr_edit, db_path = dir)
                  
                  # write.csv(pr_edit,'C:/Users/jaett/Documents/DT_test.csv', row.names = FALSE)
                  
                  
                  
                  }
    if (j == 1) {print('drug_id is not an editable column')}
    print(paste(toString(i), toString(j), k))
  })
  
  output$new_diag_pharm_update <- renderUI({
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull(substr(Sys.Date(), 1, 4), db_path = dir)
    diagnosis_choices <- diagnosis_drug_ref$diagnosis
    
    
    selectizeInput("new_diag_pharm_update", 
                "Select Diagnosis",
                choices = c(" ", diagnosis_choices),
                multiple=TRUE,
                options = list(create = TRUE))
    
    
  })
  
  observeEvent(input$create_new_drug_btn, {
    showModal(modalDialog(
      title = "Add a New Drug to Pharmacy",
      fluidRow(column(3, uiOutput("new_diag_pharm_update")),
               column(3, textInput("new_drug_name","Drug Name", "")),
               column(2, textInput("new_dosage","Dosage", "")),
               column(2, textInput("new_ordered","Ordered", "")),
               column(2, textInput("new_dist","Distributed", "")),),
      
      footer = fluidRow(column(1, offset = 7, actionButton('add_drug_btn','Add Drug')),
                        column(1, style='padding-left:75px;', modalButton("Cancel")))
    ))
  })
  
  observeEvent(input$add_drug_btn, {
    
    #if pharm_stage doesn't exist already then create it
    pr_edit <- diagdrug_pull$pharm_stage_view(db_path = dir)
    if(length(pr_edit) == 0){pr_edit <- diagdrug_pull$pharm_recordviewer(toString(input$pharm_refyr_slt), db_path = dir)
                             diagdrug_pull$pharm_update_staging(pr_edit, db_path = dir)}
    
    
    # [['drug_id', 'year', 'drug_name', 'dosage', 'ordered', 'distributed', 'stage_update']]
    if (toString(input$pharm_newyr_slt) == '') {stageyr <- toString(input$pharm_refyr_slt)} else {stageyr <- toString(input$pharm_newyr_slt)}
    pharmadd <- data.frame(stageyr, toString(input$new_drug_name), toString(input$new_dosage), toString(input$new_ordered), toString(input$new_dist))
    names(pharmadd) <- c("year", "drug_name", "dosage","ordered", "distributed")
    print(pharmadd)
    diagdrug_pull$add_new_pharm(stageyr, pharmadd,list(input$new_diag_pharm_update), db_path = dir)
    
    removeModal()
    
  })
  
  observeEvent(input$sub_pharm_btn, {
    
    if(input$pharm_newyr_slt == ''){yr <- toString(input$pharm_refyr_slt)} 
    else {yr <- toString(input$pharm_newyr_slt)}
    
    res <- diagdrug_pull$pharm_submit(yr, db_path = dir)
    diagdrug_pull$clear_pharm(db_path = dir)
    
    showModal(modalDialog(
      title = "Message",
      res,
      footer = modalButton("Ok")
    ))
    
    print(res)
    
  })
  
}

options(warn = -1)
options(shiny.host = '0.0.0.0')
options(shiny.port = 1111)
shinyApp(ui, server)
