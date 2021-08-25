#!/usr/bin/env python
import os
import os.path
from os import path
import time
import argparse
import socket
from zipfile import ZipFile
import subprocess
import sys

################ - code to get hostname ##################
hostname = socket.gethostname()
print("\nTest will execute on : "+hostname)


################ - code to check if silkperformer is already running on server ##################
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

if process_exists('performer.exe'):
    sys.exit("Silkperformer process is already running on "+hostname+"\n\n\t\t Exiting...\n")
else:
    print("\nNo Silkperformer process is running on "+hostname)



################ - code to take project name and workload name as arugments to file ##############
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--projectname')
    parser.add_argument('-w', '--workloadname')
    parser.add_argument('-r', '--repo')
    args = parser.parse_args()
    print('\nSelected project is '+args.projectname)
    print('\nSelected workload is '+args.workloadname)
    print('\nselected result repo is '+ args.repo)
    
################ - code to define all directory and file paths ##############
    silk_path = 'E:\Silk\\"Silk Performer 20.5\"'
    project_path = '"E:\Silk\Projects\CSI2_Legacy2019\\'+args.projectname+'.ltp"'
    result_dir2= "E:\Silk\Projects\CSI2_Legacy2019\\"+args.repo
    workload = ' /WL:"'+args.workloadname+'"'

silk_exe = silk_path+"\\Performer.exe"
prj_arg = " "+project_path+" "
auto_rate = r' /Automation 30'

result_dir_arg=" /Resultsdir:\""+result_dir2+"\" "

tsd_result_file= "m@"+hostname+"@"+args.projectname+".tsd"
csv_result_file = "m@"+hostname+"@"+args.projectname+".csv"
zip_result_file = "m@"+hostname+"@"+args.projectname+".zip"
Tsd2Csv_path = silk_path+'\Tsd2Csv.exe'
jenkins_workspace_path = 'E:\\SCM\\workspace\\PRM\\Titanium\\Testing\\SilkPerf03VM_Test\\' 
zip_exe = 'C:\\"Program Files\"\\7-Zip\\7z.exe'

arg_execute_test = silk_exe+prj_arg+auto_rate+workload+result_dir_arg
arg_tsd_file_path = result_dir2+'\\'+tsd_result_file
arg_csv_file_path = result_dir2+'\\'+csv_result_file
arg_convert_to_csv = Tsd2Csv_path+" "+arg_tsd_file_path+" "+arg_csv_file_path
print("\n")
print("\nBelow is silkperformer test execution command")
print(arg_execute_test)
print("\n")
time.sleep(10)
print("Starting Execution . . .")
#################### - below OS command executes silk performer test - #######################
os.system(arg_execute_test)
file_status1 = str(path.exists(result_dir2+'\\projectSettings.xml'))
if path.exists(result_dir2+'\\projectSettings.xml'):
    print('\nTest started successfully')
else:
    sys.exit('\nTest could not be started successfully for some reason')

print("\nExecution Completed!")
print("")
#################### - Below code is to get csv file , zip and send it to jenkins folder - ##########

print("This is result file path : "+arg_tsd_file_path)
print("\nConverting .tsd file to .csv")

print(arg_convert_to_csv)
print("")
file_status = str(path.exists(arg_tsd_file_path))

while file_status == "False":
    print("Wait for result file to be generated...")

    time.sleep(30)

    file_status = str(path.exists(arg_tsd_file_path))
else:
     if os.path.isfile(arg_csv_file_path):
        print("result csv already exists")
     else:
       
        os.system(arg_convert_to_csv)
        print(".csv result file created successfully")
        print("zipping...")
        os.system(zip_exe+" a "+result_dir2+"\\"+zip_result_file+" "+arg_csv_file_path)
        os.system("copy "+result_dir2+"\\"+zip_result_file+" "+jenkins_workspace_path)





