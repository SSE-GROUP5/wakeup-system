import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from triggers_gui_config.triggers_gui_config import tkinter_configuration

def run_interactive_device():
    print("Running interactive device")
    


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    
    # check if --no-gui flag is present
    if "--no-gui" in sys.argv:
        run_interactive_device()
    else:
        # run the gui
        tkinter_configuration(os.path.join(current_path, ".env.wakeup"), ["TIMEOUT", "FRAME_RATE"])
        run_interactive_device()