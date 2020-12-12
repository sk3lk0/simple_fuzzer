import os
import shutil
import subprocess
import time
from datetime import datetime


def create_new():
    with open(trash, "wb") as f:
        data = os.urandom(4096)
        f.write(data)
    return data


cdb = "cdb.exe"  # cdb
program = "program"
crashdir = "C:\\"
trash = "trash"

def startapp(trash):
    print()
    cmd = cdb + ' ' + '-c ".logopen ' + crashdir + 'temp.log;g;.logclose ' + crashdir + 'temp.log" ' + program + ' ' + trash
    process = subprocess.Popen(cmd)
    return process


def kill(proc_obj):
    proc_obj.terminate()


def wascrash():
    log = open(crashdir + 'temp.log').read()
    if "Access violation - code" in log:
        return True


def dumpcrash(crash_filename):
    prog = program.split('\\')[-1:][0]
    shutil.copyfile(crash_filename, crashdir + prog + '_' + datetime.now().strftime("%y-%m-%d-%H:%M:%S") + '_Crash' + ".txt")


fuzz = (program, crashdir, cdb)  # Initialize the fuzzer
while True:
    create_new()
    proc = startapp(trash)
    time.sleep(2)  # Run the prog for 2 seconds
    kill(proc)  # Kill() => Kill the prog. process
    if wascrash() == True:  # wascrash() return True if the prog. crashed last time
        print("Crashed")
        dumpcrash(trash) # Will copy the test case causing the crash to log folder "crashdir"
