import os
import time
import psutil


def kill(procname):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == procname:
            proc.kill()


def init_display():
    download_meme = "curl -X GET 'https://meme-api.herokuapp.com/gimme' | jq '.url' | xargs wget -O meme"
    show_meme = "sxiv -a -f -s f meme &"
    os.system(download_meme)
    while True:
        os.system(show_meme)
        os.system(download_meme)
        time.sleep(5)
        kill("sxiv")


def show_meme(self):
    pass


try:
    init_display()
except KeyboardInterrupt:
    kill("sxiv")