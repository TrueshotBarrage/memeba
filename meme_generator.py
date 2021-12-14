import os
import time
import psutil


class MemeGenerator():
    def __init__(self):
        self.download0 = (
            "curl -X GET 'https://meme-api.herokuapp.com/gimme' | "
            "jq '.url' | xargs wget -O meme0 &")
        self.download1 = (
            "curl -X GET 'https://meme-api.herokuapp.com/gimme' | "
            "jq '.url' | xargs wget -O meme1 &")
        self.show0 = "sxiv -a -f -s f meme0 &"
        self.show1 = "sxiv -a -f -s f meme1 &"
        self.state = False

        # Pre-download the meme
        os.system(self.download0)
        self.default_meme()

    def kill(self, procname):
        """Kill all system processes that match the process name.
        
        Args:
            procname (str): The name of the processes to be killed
        """
        for proc in psutil.process_iter():
            # Check whether the process name matches
            if proc.name() == procname:
                proc.kill()

    def show_meme(self, display_duration=5):
        if self.state:
            os.system(self.show1)
            os.system(self.download0)
        else:
            os.system(self.show0)
            os.system(self.download1)

        self.state = not self.state
        time.sleep(display_duration)

    def default_meme(self):
        default_dir = os.path.join("/home", "pi", "memeba", "assets",
                                   "default.png")
        os.system(f"feh -F -Z {default_dir} &")

    def cleanup(self):
        self.kill("sxiv")
        self.kill("feh")
        os.system("rm meme0; rm meme1")
