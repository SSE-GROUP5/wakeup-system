# Example usage at the bottom of the file

import tkinter as tk
from gui_utils import add_bottom_label_with_button, get_env_vars, add_env_vars_to_gui, add_dropdown_menu
from env_vars_utils import read_env_file

WAKEUP_SERVER_URL = "WAKEUP_SERVER_URL"

# GUI
def tkinter_configuration(filename, necessary_env_vars, env_var_validation=None):
    """
    This function creates a tkinter window for the user to enter the necessary environment variables
      :param necessary_env_vars: A list of the necessary environment variables
      :param env_var_validation: A function that takes in a dict of the environment variables and must return a boolean
    """
    
    # Create the main window
    necessary_env_vars.append(WAKEUP_SERVER_URL)
    
    root = tk.Tk()
    root.title("Wakeup Server Configuration")
    root.geometry(f"400x{70 + (50 * len(necessary_env_vars))}")

    labels = []
    entries = []

    already_env_vars = read_env_file(filename)
    device_id = get_env_vars(filename, "DEVICE_ID")
    
    label_type, var = add_dropdown_menu(root, filename, necessary_env_vars)
    labels.append(label_type)
    entries.append(var)
    
    labels, entries = add_env_vars_to_gui(necessary_env_vars, already_env_vars, root, labels, entries)
    
    message_label = tk.Label(root, text="", fg="red")
    add_bottom_label_with_button(root, filename, necessary_env_vars, labels, entries, message_label, env_var_validation, device_id)
    
    root.mainloop()
    
    


if __name__ == "__main__":
    # Example usage
    
    ## Validation example callback
    def env_var_validation(dict_of_env_vars):
        if not dict_of_env_vars["TIMEOUT"].isdigit() or int(dict_of_env_vars["TIMEOUT"]) <= 0:
            return False
        if not dict_of_env_vars["FRAME_RATE"].isdigit() or int(dict_of_env_vars["FRAME_RATE"]) <= 0:
            return False
        return True
    
    tkinter_configuration(".env.wakeup", ["TIMEOUT", "FRAME_RATE"], env_var_validation)