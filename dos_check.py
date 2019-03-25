import subprocess, sys, os
import time

os.system("rm -f Log_cpu_memory.txt.txt")
os.system("rm -f Log_status_restarts.txt")

length=(len(sys.argv[1]))/2


f1=open("Log_cpu_memory.txt","w+")
f1.write("DATE\t   TIME\t")
for i in range(length-2):
  f1.write(" ")
f1.write("NAME\t")
for i in range(length-2):
  f1.write(" ")
f1.write("\t\tCPU(core)\tMEMORY(bytes)\n")
f1.close()

f2=open("Log_status_restarts.txt","w+")
f2.write("DATE\t   TIME\t")
for i in range(length-2):
  f2.write(" ")
f2.write("NAME\t")
for i in range(length-2):
  f2.write(" ")
f2.write("\t\tSTATUS\t\tRESTART\n")
f2.close()


cmd1 = "kubectl top pod "
cmd2 = "kubectl get pod "
cmd3 = " | awk NR==2'{print $1,$2+0,$3+0}' OFS='\t\t' | xargs -IL date +\"%Y/%m/%d %H:%M:%S L\" >> Log_cpu_memory.txt"
cmd4 = " | awk NR==2'{print $1,$3,$4}' OFS='\t\t' | xargs -IL date +\"%Y/%m/%d %H:%M:%S L\" >> Log_status_restarts.txt"

i=0
while true:
  out1 = subprocess.check_output(cmd1+sys.argv[1]+cmd3,shell=True, stderr=subprocess.PIPE)
  out2 = subprocess.check_output(cmd2+sys.argv[1]+cmd4,shell=True, stderr=subprocess.PIPE)
  i=i+1
  #time.sleep(5)


