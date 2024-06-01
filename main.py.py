import sys
import pyMeow as pm
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import importlib.util
from pynput import keyboard

# Debug print
print("Script started")

# Initialize process and base
try:
    proc = pm.open_process("ac_client.exe")
    base = pm.get_module(proc, "ac_client.exe")["base"]
    print("Process and base initialized")
except Exception as e:
    print(f"Error initializing process and base: {e}")
    sys.exit(e)

# Define pointers and offsets
class Pointer:
    local_player = 0x0017E0A8
    entity_list = 0x18AC04
    fov = 0x18A7CC
    player_count = 0x18AC0C

class Offsets:
    health = 0xEC
    armor = 0xF0
    name = 0x205

    pos_x = 0x2C
    pos_y = 0x30
    pos_z = 0x28

    head_pos_x = 0x4
    head_pos_y = 0xC
    head_pos_z = 0x8

    camera_x = 0x34
    camera_y = 0x38

    assault_rifle_ammo = 0x140
    submachine_gun_ammo = 0x138
    sniper_ammo = 0x13C
    shotgun_ammo = 0x134
    pistol_ammo = 0x12C
    grenade_ammo = 0x144

    fast_fire_assault_rifle = 0x164
    fast_fire_sniper = 0x160
    fast_fire_shotgun = 0x158

    auto_shoot = 0x204

# Define cheat functions
def set_god_mode():
    try:
        local_player = pm.r_int(proc, base + Pointer.local_player)
        pm.w_int(proc, local_player + Offsets.health, 999999)
        print("God Mode activated: Health set to 999999")
    except Exception as e:
        print(f"Error setting health: {e}")

def set_infinite_ammo():
    try:
        local_player = pm.r_int(proc, base + Pointer.local_player)
        ammo_offsets = [
            Offsets.assault_rifle_ammo, Offsets.submachine_gun_ammo,
            Offsets.sniper_ammo, Offsets.shotgun_ammo,
            Offsets.pistol_ammo, Offsets.grenade_ammo
        ]
        for offset in ammo_offsets:
            pm.w_int(proc, local_player + offset, 999999)
        print("Infinite Ammo activated: Ammo set to 999999 for all guns")
    except Exception as e:
        print(f"Error setting ammo: {e}")

def adjust_fov(new_fov):
    try:
        pm.w_float(proc, base + Pointer.fov, new_fov)
        print(f"FOV set to {new_fov}")
    except Exception as e:
        print(f"Error adjusting FOV: {e}")

def reset_health_and_ammo():
    try:
        local_player = pm.r_int(proc, base + Pointer.local_player)
        pm.w_int(proc, local_player + Offsets.health, 100)
        ammo_offsets = [
            Offsets.assault_rifle_ammo, Offsets.submachine_gun_ammo,
            Offsets.sniper_ammo, Offsets.shotgun_ammo,
            Offsets.pistol_ammo, Offsets.grenade_ammo
        ]
        for offset in ammo_offsets:
            pm.w_int(proc, local_player + offset, 30)
        print("Health and ammo reset to default values")
    except Exception as e:
        print(f"Error resetting health and ammo: {e}")

def on_press(key):
    try:
        if key == keyboard.Key.f1:
            set_god_mode()
        elif key == keyboard.Key.f2:
            set_infinite_ammo()
        elif key == keyboard.Key.f5:
            reset_health_and_ammo()
    except AttributeError:
        pass

# Custom script handling
custom_script_module = None

def import_custom_script(file_path):
    global custom_script_module
    spec = importlib.util.spec_from_file_location("custom_script", file_path)
    custom_script_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_script_module)
    print(f"Custom script {file_path} loaded")

def run_custom_script():
    if custom_script_module:
        if hasattr(custom_script_module, 'main'):
            threading.Thread(target=custom_script_module.main).start()
            print("Custom script executed")
        else:
            messagebox.showerror("Error", "The custom script does not have a 'main' function")
    else:
        print("No custom script loaded")

# GUI setup
def create_gui():
    print("Creating GUI")
    root = tk.Tk()
    root.title("AssaultCube Cheat Menu")

    # Instructions
    tk.Label(root, text="Press F1 to activate God Mode").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(root, text="Press F2 to activate Infinite Ammo").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(root, text="Press F5 to reset Health and Ammo").grid(row=2, column=0, padx=10, pady=10)

    # FOV Slider
    tk.Label(root, text="Adjust FOV:").grid(row=3, column=0, padx=10, pady=10)
    fov_slider = tk.Scale(root, from_=10, to=170, orient=tk.HORIZONTAL, command=lambda v: adjust_fov(float(v)))
    fov_slider.set(90)  # Default FOV value
    fov_slider.grid(row=3, column=1, padx=10, pady=10)

    # Custom Script Loader and Runner
    tk.Button(root, text="Load Custom Script", command=lambda: load_custom_script()).grid(row=4, column=0, padx=10, pady=10)
    tk.Button(root, text="Run Custom Script", command=lambda: run_custom_script()).grid(row=4, column=1, padx=10, pady=10)

    # Output Window
    output_frame = tk.Frame(root)
    output_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
    output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=15)
    output_text.grid(row=0, column=0, padx=10, pady=10)

    # Redirect print to the output window
    class PrintToTkinter:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, message):
            self.text_widget.insert(tk.END, message)
            self.text_widget.see(tk.END)

        def flush(self):
            pass

    sys.stdout = PrintToTkinter(output_text)
    sys.stderr = PrintToTkinter(output_text)

    print("GUI created, starting mainloop")
    root.mainloop()

def load_custom_script():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        import_custom_script(file_path)

if __name__ == "__main__":
    print("Initializing GUI")

    # Start the keyboard listener in a separate thread
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    create_gui()