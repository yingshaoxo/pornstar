from moviepy.editor import VideoFileClip
import os
from auto_everything.terminal import Terminal
import logging

os.environ['KERAS_BACKEND'] = 'tensorflow'

terminal = Terminal()

# Static directory of this module
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
# Root directory of the project
ROOT_DIR = os.path.abspath(terminal.fix_path("~/Pornstar"))
# Root directory of the project
if not terminal.exists(ROOT_DIR):
    terminal.run(f"mkdir {ROOT_DIR}")

logging.basicConfig(filename=os.path.join(ROOT_DIR, "_main.log"),
                    level=logging.DEBUG, filemode='w', format='%(levelname)s - %(message)s')


def getVideoLength(path: str):
    clip = VideoFileClip(path)
    return clip.duration
