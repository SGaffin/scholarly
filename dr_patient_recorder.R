# DR Patient Med Recorder

library(shiny)
library(bslib)
library(DT)
library(reticulate)

# use_python("C:/Users/steve/anaconda3/python.exe")
use_python("C:\\Users\\jaett\\anaconda3\\python.exe")

diagdrug_pull <- import_from_path("dr_patient_modules","C:/Users/jaett/Documents/GitHub/scholarly/utils")
# diagdrug_pull <- import_from_path("dr_patient_modules","./utils/")

# diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
# meds <- rbind(diagnosis_drug_ref$drug_name[diagnosis_drug_ref$diagnosis=="Pain"])
# dist <- rbind(diagnosis_drug_ref$distribution[diagnosis_drug_ref$drug_name=='Acetaminophen (children)'])

ui <- fluidPage(
  
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
             fluidRow(column(2, textInput("age_input","Age", "")), 
                      column(2, style='padding-left:0px;', selectInput("sex","Sex", c("Male"="M","Female"="F"))), 
                      column(2, style='padding-left:0px;', textInput("wt_input","Weight", "")),
                      column(2, style='padding-left:0px;', textInput("hr_input","Heart Rate", "",))), 
             fluidRow(column(2, textInput("bp_input","Blood Pressure", "",)), 
                      column(2, style='padding-left:0px;', textInput("rr_input","Resp Rate", "",)),
                      column(2, style='padding-left:0px;', textInput("o2s_input","O2 Sat", "",))),
             fluidRow(column(12,uiOutput("l2_txt"))),
             fluidRow(column(12,uiOutput("diagdrug_txt1"))),
             fluidRow(column(12,uiOutput("diagdrug_txt2"))),
             fluidRow(column(4,uiOutput('slt_diag_np')), column(4,uiOutput('slt_drug_np'))),
  
             fluidRow(style = 'padding-left: 15px; padding-right: 15px;', textAreaInput("proc","Procedures", "",'100%' ,'100px')),
             fluidRow(style = 'padding-left: 15px; padding-right: 15px;', textAreaInput("notes","Notes", "",'100%' ,'100px')),
             
             ),
    tabPanel('Record Viewer',
             fluidRow(column(12,style = 'padding-left: 0px;',uiOutput(('patient_records_tbl'))))
             ),
    tabPanel('Reference Table',
             fluidRow(column(12,uiOutput(('diag_drug_ref_tbl'))))
    )  
  )
  
)
server <- function(input, output, session) {
  
  # load("working_dataset.RData")
  
  
  output$titletext <- renderUI({HTML(paste('<p style="font-size:25px;"><br><b>DR Patient Medical Recorder/Viewer Tool<b></p><br>'))})
  
  output$vitals_txt <- renderUI({HTML(paste('<p style="font-size:15px;"><br><b>VITALS<b></p><br>'))})
  output$l1_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  output$l2_txt <- renderUI({HTML(paste('<p style="font-size:15px;">________________________________________________________________________________________________________</p>'))})
  
  output$diagdrug_txt1 <- renderUI({HTML(paste('<p style="font-size:15px;"><br><b>Enter Diagnosis and Select Corresponding Drug</b></p>'))})
  output$diagdrug_txt2 <- renderUI({HTML(paste('<p style="font-size:12px;">NOTE: you may submit as many diagnoses as needed per patient<b></p><br>'))})
  
  output$slt_diag <- renderUI({
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
    diagnosis_choices <- diagnosis_drug_ref$diagnosis
    
    
    selectInput("slt_diag", 
                "Select Diagnosis", 
                choices = diagnosis_choices)#c("euro", "mtcars", "iris"))
    
  })
  

  output$slt_med <- renderUI({
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
    meds <- rbind(diagnosis_drug_ref$drug_name[diagnosis_drug_ref$diagnosis==input$slt_diag])
    
    selectInput("slt_med", 
                "Select Drug", 
                choices = meds)#c("euro", "mtcars", "iris"))
    })



  output$distribution_txt <- renderUI({
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
    dose <- rbind(diagnosis_drug_ref$dosage[(diagnosis_drug_ref$diagnosis==input$slt_diag) & (diagnosis_drug_ref$drug_name==input$slt_med)])
    dist <- rbind(diagnosis_drug_ref$distribution[(diagnosis_drug_ref$diagnosis==input$slt_diag) & (diagnosis_drug_ref$drug_name==input$slt_med)])    
    
    HTML(paste('<br><p style="font-size:15px;"><b>Dosage:</b> ',dose,'<br><b>Distribution:</b> ',dist,'</p>'))
    
    })
  
  # output$diag_drug_ref_tbl = renderDT({
  #   
  #   diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
  #   diagnosis_drug_ref[c("diagnosis","drug_name","dosage","distribution")]
  #   
  # })

  output$diag_drug_ref_tbl <- renderUI({
      ddr <- diagdrug_pull$diagdrug_pull()
      ddr <- ddr[c("diagnosis","drug_name","dosage","distribution")]
    
      DT::renderDataTable(ddr, rownames = FALSE,
                               options = list(autoWidth = TRUE,
                                              pageLength = 100))  
  })
  
  # output$df = DT::renderDataTable(df, rownames = FALSE,
  #                                 options = list(
  #                                   autoWidth = TRUE,
  #                                   columnDefs = list(list(width = '10px', targets = c(1,3)))))
  
  output$patient_records_tbl <- renderUI({
    pr <- diagdrug_pull$patientrecord_pull()
    # pr <- pr[c("diagnosis","drug_name","dosage","distribution")]
    
    DT::renderDataTable(pr, rownames = FALSE,
                        options = list(autoWidth = TRUE,
                                       pageLength = 100))  
  })
  
  
  output$br_text <- renderUI({HTML(paste('<br>'))})
  
  output$slt_diag_np <- renderUI({
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
    diagnosis_choices <- diagnosis_drug_ref$diagnosis
    
    
    selectInput("slt_diag_np", 
                "Select Diagnosis", 
                choices = diagnosis_choices)
    
  })
  
  output$slt_drug_np <- renderUI({
    
    diagnosis_drug_ref <- diagdrug_pull$diagdrug_pull()
    meds <- rbind(diagnosis_drug_ref$drug_name[diagnosis_drug_ref$diagnosis==input$slt_diag_np])
    
    selectInput("slt_drug_np", 
                "Select Drug", 
                choices = meds)#c("euro", "mtcars", "iris"))
  })
  
  
  
}

options(shiny.host = '0.0.0.0')
options(shiny.port = 1111)
shinyApp(ui, server)