@echo off
start http://192.168.1.90:1111/
"C:\Program Files\R\R-4.4.2\bin\RScript.exe" -e "shiny::runApp('C:/Users/jaett/Documents/GitHub/scholarly/dr_patient_recorder.R')"
