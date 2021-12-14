import os
import time
import psutil


class MemeGenerator():
    def __init__(self):
        self.download = ("curl -X GET 'https://meme-api.herokuapp.com/gimme' | "
                         "jq '.url' | xargs wget -O meme &")
        self.show = "sxiv -a -f -s f meme &"

        # Pre-download the meme
        os.system(self.download)
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
        os.system(self.show)
        os.system(self.download)
        time.sleep(display_duration)

    def default_meme(self):
        default_dir = os.path.join("/home", "pi", "memeba", "assets",
                                   "default.png")
        os.system(f"feh -F -Z {default_dir} &")

    def cleanup(self):
        self.kill("sxiv")
        self.kill("feh")
        os.system("rm meme")


mg = MemeGenerator()
mg.show_meme()
mg.show_meme()