import subprocess, sys, os
import time

#Deleting and Creating html files

os.system("rm -f Verdict.html")
os.system("rm -f Log_Verdict.html")
f1 = open("Verdict.html","a")
f = open("Log_Verdict.html","a")

#Shell commands used

cmd1 = "grep "
cmd2 = " Log_cpu_memory.txt | awk NR=="
cmd3 = " Log_status_restarts.txt | awk NR=="
cmd4 = "'{if ($4 >= "
cmd5 = "'{if ($5 >= "
cmd6 = " Log_status_restarts.txt | awk NR=="
result = ""

#Collect Number of lines in the log files

lines1 = int(subprocess.check_output("awk 'END {printf NR}' Log_cpu_memory.txt",shell=True, stderr=subprocess.PIPE))
print(lines1)

lines2 = int(subprocess.check_output("awk 'END {printf NR}' Log_status_restarts.txt",shell=True, stderr=subprocess.PIPE))
print(lines2)

#Creating Lists for parameters
cpu = []
memo = []
status = []
restarts = []
i = 1
j = 1

for i in range(lines1 - 1):
  k = str(i+1)
  temp = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+"'{printf $4}'",shell=True, stderr=subprocess.PIPE)
  cpu.append(int(temp.strip()))
  temp = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+"'{printf $5}'",shell=True, stderr=subprocess.PIPE)
  memo.append(int(temp.strip()))

print(cpu)
print(memo)

for j in range(lines2 - 1):
  k = str(j+1)
  temp = subprocess.check_output(cmd1+sys.argv[1]+cmd3+k+"'{printf $4}'",shell=True, stderr=subprocess.PIPE)
  status.append(temp.strip())
  temp = subprocess.check_output(cmd1+sys.argv[1]+cmd3+k+"'{printf $5}'",shell=True, stderr=subprocess.PIPE)
  restarts.append(int(temp.strip()))

print(status)
print(restarts)



###############################################
#Verdict Analysis
###############################################

#Analysing parameters from Log files collected

max_cpu = max(cpu)
avg_cpu = sum(cpu)/(len(cpu))
min_cpu = min(cpu)
max_memo = max(memo)
avg_memo = sum(memo)/(len(memo))
min_memo = min(memo)
no_of_restarts = max(restarts)
thresh_cpu = int(sys.argv[2])
thresh_memo = int(sys.argv[3])
count_memo = len([x for x in memo if x >= thresh_memo])
print(count_memo)
count_cpu = len([x for x in cpu if x >= thresh_cpu])
print(count_cpu)
count_status = len([x for x in status if x != "Running"])
print(count_status)


#Create Verdict.html file

def create_verdict( result ):
  f1.write("<html><head></head><body>")
  f1.write("<h1 style=\"color: "+result+";\"><u>DOS ATTACK</u></h1>")
  f1.write("<table cellpadding=\"5\" style=\"font-size: 20; text-align: left; border-width:thick;\"><tr><th style=\"background-color: "+result+";color: white;\">Service Name : </th><td>"+sys.argv[1]+"</td></tr>")
  if(result == "#23850B"):
    f1.write("<tr><th style=\"background-color: "+result+"; color: white;\" >Verdict : </th><td>PASS</td></tr>")
    f1.write("<tr><th style=\"background-color: "+result+"; color: white;\" >Link for Log Verdict File : </th><td><a href=\"Log_Verdict.html\"><b>Click Here</b></a></td></tr>")
  elif(result == "#AA0000"):
    f1.write("<tr><th style=\"background-color: "+result+"; color: white;\" >Verdict : </th><td>FAIL</td></tr>")
    f1.write("<tr><th style=\"background-color: "+result+"; color: white;\" >Link for Log Verdict File : </th><td><a href=\"Log_Verdict.html\"><b>Click Here</b></a></td></tr>")
  f1.write("</table></body></html>")
  f1.close()

#Create Log_Verdict.html file

def create_log_verdict( result ):
  
  #Printing Basic analysis table  

  f.write("<table border=1 cellpadding=\"5\" style=\"text-align: center;\"><tr><th></th><th style=\"background-color: "+result+";color: white;\">Average</th><th style=\"background-color: "+result+";color: white;\">Maximum</th><th style=\"background-color: "+result+";color: white;\">Minimum</th></tr>")
  f.write("<tr><th style=\"background-color: "+result+";color: white;\">CPU </th><td>"+str(avg_cpu)+" </td><td>"+str(max_cpu)+" </td><td>"+str(min_cpu)+"</td></tr>")
  f.write("<tr><th style=\"background-color: "+result+";color: white;\">Memory </th><td>"+str(avg_memo)+" </td><td>"+str(max_memo)+" </td><td>"+str(min_memo)+"</td></tr></table>")
  f.write("<h4>Number of restarts : "+str(no_of_restarts)+"</h4>")
  f.write("<H2>=======================================</H2>")  

  #Checking for CPU Status if it was not Running

  if(result == "#AA0000"):
    f.write("<h1 style=\"color: "+result+";\">CPU STATUS</h1>") 
    f.write("<h3>Number of times CPU stopped running : "+str(count_status)+"</h3>")  
    if([x for x in status if x != "Running"]):      
      f.write("<table border=1 cellpadding=\"5\" style=\"text-align: center;\"><tr style=\"background-color: #AA0000;color: white;\"><th>Date</th><th>Time</th><th>Status</th></tr>")
      for i in range(lines1 - 1):
        k = str(i+1)
        dt_status = subprocess.check_output(cmd1+sys.argv[1]+cmd6+k+"'{if ($4 != \"Running\"){print $1}}' OFS='\t'",shell=True, stderr=subprocess.PIPE)
        if(dt_status != ""):
          f.write("<tr><td>"+dt_status+"</td>")
          tm_status = subprocess.check_output(cmd1+sys.argv[1]+cmd6+k+"'{if ($4 != \"Running\"){print $2}}' OFS='\t'",shell=True, stderr=subprocess.PIPE)
          f.write("<td>"+tm_status+"</td>")
          invalid_status = subprocess.check_output(cmd1+sys.argv[1]+cmd6+k+"'{if ($4 != \"Running\"){print $4}}' OFS='\t'",shell=True, stderr=subprocess.PIPE)
          f.write("<td>"+invalid_status+"</td></tr>")
      f.write("</table>")
    f.write("<H2>=======================================</H2>")
  
  #Checking for CPU exceeding threshold

  f.write("<h1 style=\"color: "+result+";\">CPU</h1>")
  f.write("<h4>Threshold of CPU : "+str(thresh_cpu)+"</h4>")
  f.write("<h4>Number of times CPU Utilization crossed threshold : "+str(count_cpu)+"</h4>")
  if(count_cpu > 0):
    f.write("<table border=1 cellpadding=\"5\" style=\"text-align: center;\"><tr style=\"background-color: #AA0000;color: white;\"><th>Date</th><th>Time</th><th>Utilization</th></tr>")
    for i in range(lines1 - 1):
      k = str(i+1)
      dt_cpu = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+cmd4+str(thresh_cpu)+"){print $1} else next }'",shell=True, stderr=subprocess.PIPE)
      if(dt_cpu != ""):
        f.write("<tr><td>"+dt_cpu+"</td>")
        tm_cpu = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+cmd4+str(thresh_cpu)+"){print $2} else next }'",shell=True, stderr=subprocess.PIPE)
        f.write("<td>"+tm_cpu+"</td>")
        thresh_exceed_cpu = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+cmd4+str(thresh_cpu)+"){print $4} else next }'",shell=True, stderr=subprocess.PIPE)
        f.write("<td>"+thresh_exceed_cpu+"</td></tr>")
    f.write("</table>")
  f.write("<H2>=======================================</H2>")

  #Checking for Memory exceeding threshold

  f.write("<h1 style=\"color: "+result+";\">MEMORY</h1>")
  f.write("<h4>Threshold of Memory : &nbsp;"+str(thresh_memo)+"</h4>")
  f.write("<h4>Number of times Memory Utilization crossed threshold : "+str(count_memo)+"</h4>")
  if(count_memo > 0):
    f.write("<table border=1 cellpadding=\"5\" style=\"text-align: center;\"><tr style=\"background-color: #AA0000;color: white;\"><th>Date</th><th>Time</th><th>Utilization</th></tr>")
    for i in range(lines1 - 1):
      k = str(i+1)
      dt_memo = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+cmd5+str(thresh_memo)+"){print $1} else next }'",shell=True, stderr=subprocess.PIPE)
      if(dt_memo != ""):
        f.write("<tr><td>"+dt_memo+"</td>")
        tm_memo = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+cmd5+str(thresh_memo)+"){print $2} else next }'",shell=True, stderr=subprocess.PIPE)
        f.write("<td>"+tm_memo+"</td>")
        thresh_exceed_memo = subprocess.check_output(cmd1+sys.argv[1]+cmd2+k+cmd5+str(thresh_memo)+"){print $5} else next }'",shell=True, stderr=subprocess.PIPE)
        f.write("<td>"+thresh_exceed_memo+"</td></tr>")
    f.write("</table>")
  f.write("<H2>=======================================</H2>")
  f.write("</body></html>")
  f.close()
    
#Calling the functions to check PASS/FAIL

if(count_memo!=0 or count_cpu!=0 or no_of_restarts!=0 or [x for x in status if x != "Running"]):
  print("fail")
  create_verdict("#AA0000")
  f.write("<html><head></head><body>")
  f.write("<h1 style=\"color: #AA0000;\">FAILED</h1>")
  create_log_verdict("#AA0000")
  
else:
  print("pass")
  create_verdict("#23850B")
  f.write("<html><head></head><body>")
  f.write("<h1 style=\"color: #23850B;\">PASSED</h1>")
  create_log_verdict("#23850B")
    

