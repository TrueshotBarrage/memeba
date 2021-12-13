import os
import time
import psutil


def kill(procname):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == procname:
            proc.kill()


def init_display():
    load_meme = "curl -X GET 'https://meme-api.herokuapp.com/gimme' | jq '.url' | xargs wget -O meme; sxiv -a -f -s f meme &"
    while True:
        os.system(load_meme)
        time.sleep(5)
        kill("sxiv")


try:
    init_display()
except KeyboardInterrupt:
    kill("sxiv")