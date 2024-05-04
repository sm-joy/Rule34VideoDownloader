from os.path import join
from os import getcwd

Notify_Sound: bool = True
working_dir = getcwd()
SAVE_PATH = join(working_dir, "Videos")
DRIVER_PATH = join(working_dir, "Chrome_Driver", "chromedriver.exe")
    