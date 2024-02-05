import sys
import os
from blinkDetect import main

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from triggers_gui_config.triggers_gui_config import tkinter_configuration

def run_interactive_device():
    print("Running interactive device")
    main()
    


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    
    # check if --no-gui flag is present
    if "--no-gui" in sys.argv:
        run_interactive_device()
    else:
        # run the gui
        tkinter_configuration(os.path.join(current_path, ".env.wakeup"), ["CLOSED_EYES_FRAME", "BLINKING_RATIO", "TIMEOUT_SEC"])
        run_interactive_device()