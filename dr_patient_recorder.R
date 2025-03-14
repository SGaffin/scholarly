# DR Patient Med Recorder

library(shiny)
library(shinyjs)
library(bslib)
library(DT)
library(reticulate)
library(dplyr)

# use_python("C:/Users/steve/anaconda3/python.exe")
setwd("C:/Users/jaett/Documents/GitHub/scholarly") 
use_python("C:\\Users\\jaett\\anaconda3\\python.exe")

diagdrug_pull <- import_from_path("dr_patient_modules","C:/Users/jaett/Documents/GitHub/scholarly/utils")

#make this run every time app is refreshed
cleartemps <- diagdrug_pull$cleartemps()

#runApp("dr_patient_recorder.R")

ui <- fluidPage(
  useShinyjs(),
  fluidRow(column(12,uiOutput("titletext"))),
  fluidRow(),
  tabsetPanel(
    #tabPanel('testpanel',
     #        fluidRow(column(3,uiOutput('slt_diag'))),
      #       fluidRow(column(4,uiOutput('slt_med'))),
       #      fluidRow(column(8,uiOutput("distribution_txt")))
        #    ),
    tabPanel('New Patient',
             fluidRow(column(3,uiOutput('br_text'))),
             fluidRow(column(12,uiOutput("l1_txt"))),
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
             fluidRow(column(12, uiOutput('patient_lab_res_temp'))),
             fluidRow(column(12,uiOutput("l3_txt"))),
             fluidRow(column(12,uiOutput("diagdrug_txt1"))),
             fluidRow(column(12,uiOutput("diagdrug_txt2"))),
             
             fluidRow(column(2,uiOutput('slt_diag_np')), column(2, style='padding-left:0px;',uiOutput('slt_drug_np'))),
             fluidRow(column(2, style='padding-top:20px;' ,actionButton("save_diagdrug_btn", "Add Diagnosis", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(12,uiOutput('patient_diag_drug_temp'))),
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
             fluidRow(column(12,style = 'padding-left: 0px;',uiOutput('patient_records_tbl'))),
             fluidRow(column(12,style = 'padding-left: 0px;',uiOutput('diag_drug_tbl')))
             ),
    tabPanel('Pharmacy - Admin Only',
             fluidRow(column(12,uiOutput("ws1"))),
             fluidRow(column(2, style='padding-top:20px;' ,actionButton("edit_exist_pharm_btn", "Edit Existing Pharmacy", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(2, style='padding-top:20px;' ,actionButton("create_new_pharm_btn", "Create New Pharmacy", style="background-color: gray; border-color: #2e6da4"))),
             fluidRow(column(2, style='padding-top:20px;' ,hidden(actionButton("save_pharm_changes_btn", "Save Changes", style="background-color: gray; border-color: #2e6da4")))),
             fluidRow(column(2, style='padding-top:20px;', hidden(uiOutput('pharm_refyr_slt'))),
                      column(2, style='padding-top:20px;', hidden(uiOutput('pharm_newyr_slt')))),
             fluidRow(column(12,uiOutput("ws2"))),
             # fluidRow(column(2, style='padding-top:20px;', uiOutput('pharm_yr_slt'))),
             # fluidRow(column(10, offset=1, hidden(uiOutput('pharm_ref_tbl'))))#,
             fluidRow(column(10, offset=1, dataTableOutput('pharm_ref_tbl2')))
             # fluidRow(column(10, offset=1, hidden(uiOutput('testtable'))))
             )
    # tabPanel('Reference Table',
    #          fluidRow(column(12,uiOutput('diag_drug_ref_tbl')))
    #         )  
  )
  
)
server <- function(input, output, session) {
  
  # load("working_dataset.RData")
  
  
  output$titletext <- renderUI({HTML(paste('<p style="font-size:25px;"><br><b>DR Patient Medical Recorder/Viewer Tool<b></p><br>'))})
  
  output$vitals_txt <- renderUI({HTML(paste('<p style="font-size:15px;background-color: #FFFF00;"><b>Patient Vitals<b></p><br>'))})
  output$l1_txt <- renderUI({HTML(paste('<p style="font-size:15px; margin-bottom: -10px;">________________________________________________________________________________________________________</p>'))})
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
  
  output$ws1 <- renderUI({HTML(paste0('<br><br>'))})
  output$ws2 <- renderUI({HTML(paste0('<br><br>'))})
  
  # output$patient_vitals_temp <- renderUI({tryCatch(
  #                                           expr = {pvtemp <- diagdrug_pull$patient_vitals_staging(isolate(input$fname_input),isolate(input$lname_input),isolate(input$age_input),
  #                                                                                        isolate(input$sex_input),isolate(input$wt_input),isolate(input$hr_input),
  #                                                                                        isolate(input$bp_input),isolate(input$rr_input),isolate(input$o2s_input))
  #                                                   print(toString(nrow(pvtemp)))
  #                                                   pvtemp <- pvtemp[c("first_name","last_name","age","sex", 'heart_rate','blood_pressure','resp_rate','O2_sat','weight')]
  #                                                   renderDT(pvtemp, rownames = FALSE, selection = 'single', options = list(dom = 't'))},
  #                                           error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))}
  #                                           )
  #                                         })
  
  

  

 # output$patient_diag_drug_temp <- renderUI({input$save_diagdrug_btn
 #   
 #                                             tryCatch(
 #                                              expr = {pddemp <- diagdrug_pull$diag_drug_staging(isolate(input$slt_diag_np),isolate(input$slt_drug_np))
 #                                                      pddemp <- pddemp[c("diagnosis","drug")]
 # 
 # 
 #                                                      renderDT(pddemp, rownames = FALSE, selection = 'single', options = list(dom = 't'))
 #                                                      },
 #                                              error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))}
 #                                            )
 # 
 #                                              })
  
  observeEvent(input$save_diagdrug_btn, {

                                    tryCatch(
                                      expr = {pddemp <- diagdrug_pull$diag_drug_staging(isolate(input$slt_diag_np),isolate(input$slt_drug_np))
                                      pddemp <- pddemp[c("diagnosis","drug")]


                                      output$patient_diag_drug_temp <- renderUI(renderDT(pddemp, rownames = FALSE, selection = 'single', options = list(dom = 't')))
                                      },
                                      error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))}
                                    )


                                  })
  
  # output$patient_lab_res_temp <- renderUI({input$add_lab_btn
  #   
    # tryCatch(
    #   expr = {plrtemp <- diagdrug_pull$lab_results_staging(isolate(input$slt_lab_name),isolate(input$slt_lab_val))
    #           plrtemp <- plrtemp[c("lab_name","lab_value")]
    #           renderDT(plrtemp, rownames = FALSE, selection = 'single', options = list(dom = 't'))
    #           },
    #   error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))}
    #   )
  #   
  # })
  
  observeEvent(input$add_lab_btn, {
                                    tryCatch(
                                      expr = {plrtemp <- diagdrug_pull$lab_results_staging(isolate(input$slt_lab_name),isolate(input$slt_lab_val))
                                      plrtemp <- plrtemp[c("lab_name","lab_value")]
                                      output$patient_lab_res_temp <- renderUI(renderDT(plrtemp, rownames = FALSE, selection = 'single', options = list(dom = 't')))
                                      },
                                      error = function(e){HTML(paste0('<br><p style="font-size:12px; color: red"><b>No entries have been saved</b></p>'))}
                                    )
  })
  
  
  observeEvent(input$submit_btn, {
                                  diagdrug_pull$final_submit(isolate(input$fname_input), isolate(input$lname_input), isolate(input$age_input), isolate(input$sex_input), 
                                                             isolate(input$wt_input), isolate(input$hr_input), isolate(input$bp_input), isolate(input$rr_input), isolate(input$o2s_input),
                                                             isolate(input$proc_txt), isolate(input$notes_txt), isolate(input$slt_glasses))
    
                                  updateTextInput(session, "fname_input", value = "")
                                  updateTextInput(session, "lname_input", value = "")
                                  updateTextInput(session, "age_input", value = "")
                                  updateTextInput(session, "sex_input", value = "")
                                  updateTextInput(session, "wt_input", value = "")
                                  updateTextInput(session, "hr_input", value = "")
                                  updateTextInput(session, "bp_input", value = "")
                                  updateTextInput(session, "rr_input", value = "")
                                  updateTextInput(session, "o2s_input", value = "")
                                  
                                  lab_test_ref <- diagdrug_pull$lab_tests_pull()
                                  lab_names <- unique(lab_test_ref$lab_name)
                                  updateSelectInput(session, "slt_lab_name", label = "Select Lab Test", choices = c("No Labs",lab_names))
                                  
                                  
                                  diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
                                  diagnosis_choices <- diagnosis_drug_ref$diagnosis
                                  updateSelectInput(session, "slt_diag_np", label = "Select Diagnosis", choices = c(" ", diagnosis_choices))
                                  
                                  
                                  updateTextAreaInput(session, "proc_txt", value = "")
                                  updateTextAreaInput(session, "notes_txt", value = "")
                                  
                                  updateSelectInput(session, "slt_glasses", label = "Select Glassess", choices = c("No Glasses","1.00","1.25","1.5","1.75","2.00","2.25","2.5","2.75","3.00","3.25","3.5","3.75","4.00"))
                                  
                                  cleartemps <- diagdrug_pull$cleartemps()
    
  })
  
  

  output$diag_drug_ref_tbl <- renderUI({
      ddr <- diagdrug_pull$diagdrug_pull()
      ddr <- ddr[c("diagnosis","drug_name","dosage","distribution")]
    
      DT::renderDataTable(ddr, rownames = FALSE,
                               options = list(autoWidth = TRUE,
                                              pageLength = 100))  
  })

  
  output$patient_records_tbl <- renderUI({
    pr <- diagdrug_pull$patientrecord_pull()
    # pr <- pr[c("diagnosis","drug_name","dosage","distribution")]
    
    DT::renderDataTable(pr, rownames = FALSE,
                        options = list(autoWidth = TRUE,
                                       pageLength = 100))  
  })
  
  output$diag_drug_tbl <- renderUI({
    
    dd <- diagdrug_pull$diagdrug_recordviewer()
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
    
                                    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
                                    diagnosis_choices <- diagnosis_drug_ref$diagnosis
                                    
                                    
                                    selectInput("slt_diag_np", 
                                                "Select Diagnosis", 
                                              choices = c(" ", diagnosis_choices))
                                  
                                })
  
  output$slt_drug_np <- renderUI({
    
                                  diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
                                  meds <- rbind(diagnosis_drug_ref$drug_name[diagnosis_drug_ref$diagnosis==input$slt_diag_np])
                                  
                                  selectInput("slt_drug_np", 
                                              "Select Drug", 
                                              choices = meds)
                                })
  
  
  output$slt_lab_name <- renderUI({
    
                                    lab_test_ref <- diagdrug_pull$lab_tests_pull()
                                    lab_names <- unique(lab_test_ref$lab_name)
                                    
                                    
                                    selectInput("slt_lab_name", 
                                                "Select Lab Test", 
                                                choices = c("No Labs",lab_names))
                                    
                                  })

  
  output$slt_lab_val <- renderUI({
    
                                  lab_test_ref <- diagdrug_pull$lab_tests_pull()
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
  
  

  
  output$pharm_ref_tbl2 <- renderDT({
                  
                                    tryCatch(                                
    
                                    {pr <- diagdrug_pull$pharm_recordviewer(toString(input$pharm_refyr_slt))
                                    pr[order(pr$drug_name), ]
                                    # pr <- pr[c("diagnosis","drug_name","dosage","distribution")]
                                    
                                    if(input$pharm_newyr_slt != ''){pr$year <- toString(input$pharm_newyr_slt)}
                                    
                                    DT::datatable(pr,
                                                  rownames = FALSE,
                                                  editable = TRUE,
                                                  options = list(autoWidth = TRUE,
                                                                 pageLength = 100,
                                                                 dom = 't'))
                                    },
                                    #if an error occurs, tell me the error
                                    error=function(e) {
                                      message('An Error Occurred')
                                      # print(' ')#e)
                                    },
                                    #if a warning occurs, tell me the warning
                                    warning=function(w) {
                                      message('A Warning Occurred')
                                      print(w)
                                      return(NA)
                                    })
  })
  


  
  observeEvent(input$pharm_refyr_slt, {shinyjs::show("pharm_ref_tbl2")})
  observeEvent(input$save_pharm_changes_btn, {shinyjs::show("testtable")})
  

  
  observeEvent(input$create_new_pharm_btn, {
    shinyjs::show("pharm_refyr_slt")
    shinyjs::show("pharm_newyr_slt")
    shinyjs::show("save_pharm_changes_btn")
    shinyjs::hide("edit_exist_pharm_btn")
    shinyjs::hide("create_new_pharm_btn")
    
  })

  
  output$pharm_refyr_slt <- renderUI({
    
    # pharm_yr <- diagdrug_pull$pharm_recordviewer()
    # pharm_yr <- as.list(unique(pharm_yr$year))
    
    pharm_yr <- as.list(diagdrug_pull$pharm_years())
    
    
    selectInput("pharm_refyr_slt", 
                "Select Pharmacy Reference Year", 
                choices = c("",pharm_yr))
    
  })
  
  output$pharm_newyr_slt <- renderUI({
    
    
    selectInput("pharm_newyr_slt", 
                "Select New Pharmacy Year", 
                choices = c("","2025","2026","2027", "2028","2029","2030"))
    
  })

  observeEvent(input$pharm_ref_tbl2_cell_edit, {
    
    
    print('input$pharm_ref_tbl_cell_edit')
    pr_edit <- diagdrug_pull$pharm_recordviewer(toString(input$pharm_refyr_slt))
    pr_edit[order(pr_edit$drug_name), ]

    #get values
    info = input$pharm_ref_tbl2_cell_edit
    i = as.numeric(info$row)
    j = as.numeric(info$col) + 1
    k = toString(info$value)


    #write values to reactive
    pr_edit[i,j] <- k
    
    diagdrug_pull$pharm_update_staging(pr_edit)
    
    write.csv(pr_edit,'C:/Users/jaett/Documents/DT_test.csv', row.names = FALSE)
  })
  

  
}

options(shiny.host = '0.0.0.0')
options(shiny.port = 1111)
shinyApp(ui, server)
