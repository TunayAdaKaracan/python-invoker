import os
import time
import subprocess


PROCESSES = []

CLIENT_COUNT = int(input("Client Count > "))
for i in range(CLIENT_COUNT):
    process = subprocess.Popen(['py', 'main.py', '-s'], shell=True)
    PROCESSES.append(process)

print("Waiting 5 seconds")
time.sleep(5)
print("Killing PIDS:")
for i, process in enumerate(PROCESSES):
    process.terminate()
    print(str(i)+" | Killed pid: "+str(process.pid))
