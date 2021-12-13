import os
import time


def init_display():
    os.system("tightvncserver")
    os.system("cd ~/memeba")
    load_meme = "curl -X GET 'https://meme-api.herokuapp.com/gimme' | jq '.url' | xargs wget -O meme; sxiv -a -f -s f meme"
    os.system(load_meme)
    time.sleep(5)
    os.system(load_meme)


init_display()