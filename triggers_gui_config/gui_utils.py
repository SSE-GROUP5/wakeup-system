import tkinter as tk
from .requests_utils import test_connection, create_interactive_device
from .env_vars_utils import get_env_vars

WAKEUP_SERVER_URL_INDEX = -1

# UTILS
def add_dropdown_menu(root, filename, necessary_env_vars):
    label_type = tk.Label(root, text="Enter TYPE")
    var = tk.StringVar(root)
    var.set(get_env_vars(filename, "TYPE") if get_env_vars(filename, "TYPE") else "SOUND")
    option = tk.OptionMenu(root, var, "SOUND", "VISION")
    
    label_type.grid(row=len(necessary_env_vars), column=0)
    option.grid(row=len(necessary_env_vars), column=1)
    
    return label_type, var

def add_env_vars_to_gui(env_vars, already_env_vars, root, labels, entries):
    for i, env_var in enumerate(env_vars):
        if env_var in already_env_vars:
            value = already_env_vars[env_var]
        else:
            value = ""
        label = tk.Label(root, text=f"Enter {env_var}")
        label.grid(row=i, column=0)
        entry = tk.Entry(root)
        entry.insert(0, value)
        entry.grid(row=i, column=1)
        labels.append(label)
        entries.append(entry)

    return labels, entries

def add_bottom_label_with_button(root, filename, necessary_env_vars, labels, entries, message_label, env_var_validation, device_id):
    message_label = tk.Label(root, text="", fg="red")
    button = tk.Button(root, text="Configure", command=lambda: on_configure_button_click(filename, labels, entries, root, message_label, env_var_validation, device_id))
    button.grid(row=len(necessary_env_vars)+2, column=0, columnspan=2)
    
    message_label.grid(row=len(necessary_env_vars)+3, column=0, columnspan=2)
    
    if device_id:
      label_device_id = tk.Label(root, text=f"    Device ID: {device_id}")
      label_device_id.grid(row=len(necessary_env_vars)+4, column=0, columnspan=2)

def on_configure_button_click(filename, labels, entries, root, message_label, env_var_validation=None, device_id=None):
    if env_var_validation is not None:
        labels_text = [label.cget('text').split()[1] for label in labels]
        entries_text = [entry.get() for entry in entries]
        if not env_var_validation(dict(zip(labels_text, entries_text))):
            message_label.config(text="Invalid environment variables", fg="red")
            return
  
    wakeup_server_url = entries[WAKEUP_SERVER_URL_INDEX].get()
    if wakeup_server_url:
        message_label.config(text="TRYING TO CONNECT TO SERVER...", fg="blue")
        if test_connection(wakeup_server_url):
            if device_id is None:
                message_label.config(text="CREATING DEVICE...", fg="blue")
                device_id = create_interactive_device(wakeup_server_url, entries[-1].get())
                
            message_label.config(text=f"Connection test successful. Closing the main loop.", fg="green")
            with open(filename, "w") as file:
                file.write(f"DEVICE_ID={device_id}\n")
                for label, entry in zip(labels, entries):
                    file.write(f"{label.cget('text').split()[1]}={entry.get()}\n")
                    
            root.destroy()  # Close the main loop if the connection test is successful
        else:
            print("Connection test failed. Please check the IP address and try again.")
            message_label.config(text="Connection test failed. Please check the IP address and try again.", fg="red")
    else:
        print("No IP address entered.")
        message_label.config(text="No IP address entered.", fg="red")