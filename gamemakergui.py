import time
import cv2
import numpy as np
import pyautogui
import keyboard
import secrets
import string
import tkinter as tk
from tkinter import ttk
import threading

def search_image(image_path, threshold=0.9):
    img_rgb = pyautogui.screenshot()
    img_gray = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image_path, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    return zip(*loc[::-1])

stop_script = False

def create_game():
    global stop_script

    game_name = game_name_entry.get()
    set_password = password_var.get()
    difficulty = difficulty_var.get()
    game_counter = 1

    while not stop_script:
        matches = search_image("imgs/exitlobby.png")
        for match in matches:
            gamename_matches = search_image("imgs/gamename.png")
            for gamename_match in gamename_matches:
                x, y = gamename_match
                pyautogui.click(x + 20, y + 40)
                keyboard.press('ctrl')
                pyautogui.press('a')
                keyboard.release('ctrl')
                pyautogui.press('backspace')
                current_game_name = f"{game_name}-{game_counter:02d}"
                pyautogui.typewrite(current_game_name)

                if set_password:
                    password_matches = search_image("imgs/password.png")
                    for password_match in password_matches:
                        x, y = password_match
                        pyautogui.click(x + 20, y + 40)
                        keyboard.press('ctrl')
                        pyautogui.press('a')
                        keyboard.release('ctrl')
                        pyautogui.press('backspace')
                        random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
                        pyautogui.typewrite(random_password)
                        break

                difficulty_matches = search_image(f"imgs/{difficulty}.png")
                for difficulty_match in difficulty_matches:
                    x, y = difficulty_match
                    pyautogui.click(x + 20, y + 20)
                    break

                create_matches = search_image("imgs/creategame.png")
                for create_match in create_matches:
                    x, y = create_match
                    pyautogui.moveTo(x + 20, y + 20)
                    pyautogui.click()
                    break

                game_counter += 1

            break

        time.sleep(1)

def stop_game():
    global stop_script
    stop_script = True
    
def create_game_thread():
    game_thread = threading.Thread(target=create_game, daemon=True)
    game_thread.start()

# Create the GUI window
window = tk.Tk()
window.title("Game Creator")

# Create and place widgets
game_name_label = ttk.Label(window, text="Game Name:")
game_name_label.grid(column=0, row=0, padx=5, pady=5, sticky="W")

game_name_entry = ttk.Entry(window)
game_name_entry.grid(column=1, row=0, padx=5, pady=5, sticky="W")

password_var = tk.BooleanVar()
password_checkbox = ttk.Checkbutton(window, text="Set password?", variable=password_var)
password_checkbox.grid(column=0, row=1, padx=5, pady=5, sticky="W")

difficulty_var = tk.StringVar()
difficulty_combobox = ttk.Combobox(window, textvariable=difficulty_var, values=("normal", "nightmare", "hell"))
difficulty_combobox.set("normal")
difficulty_combobox.grid(column=1, row=1, padx=5, pady=5, sticky="W")

create_button = ttk.Button(window, text="Create Game", command=create_game_thread)
create_button.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

stop_button = ttk.Button(window, text="Stop", command=stop_game)
stop_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

# Run the GUI event loop
window.mainloop()