import os
import subprocess
import time


def create_new():
    with open('mysession.nps', "wb") as f:
        data = os.urandom(4096)
        f.write(data)
    return data

def execute_fuzz(data, counter):
    process = subprocess.Popen(["programm", "arg","arg2"], shell=False, stdout=subprocess.PIPE)
    print('process created')
    time.sleep(0.5)
    crash = process.poll()
    if not crash:
        print('no crash')
        try:
            process.terminate()
        except OSError:
            pass
    else:
        print('crash')
        with open("crashes/crash.{}.txt".format(counter), "wb+") as f:
                    f.write(data)
        process.wait()


counter = 0
while counter < 100000:
    print(f'try: {counter}')
    data = create_new()
    execute_fuzz(data, counter)
    counter += 1
