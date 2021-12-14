import os
import time
from numpy.lib.function_base import disp
import psutil


class MemeGenerator():
    def __init__(self):
        self.download = ("curl -X GET 'https://meme-api.herokuapp.com/gimme' | "
                         "jq '.url' | xargs wget -O meme")
        self.display =" sxiv -a -f -s f meme &" 

    def kill(procname):
        """Kill all system processes that match the process name.
        
        Args:
            procname (str): The name of the processes to be killed
        """
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == procname:
                proc.kill()

    def show_meme(display_duration=5):
        download_meme = ("curl -X GET 'https://meme-api.herokuapp.com/gimme' | "
                         "jq '.url' | xargs wget -O meme")
        show_meme = "sxiv -a -f -s f meme &"

        os.system(download_meme)
        os.system(show_meme)
        time.sleep(display_duration)
        kill("sxiv")
        os.system("rm meme")
