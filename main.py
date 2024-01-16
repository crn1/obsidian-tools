from threading import Thread

import hotkeys
import chrome_engine
import console
import obsidian_engine

# Import all the hotkeys from hotkeys.py file
hotkeys.add_hotkeys()

# Welcome to Obsidian Tools!
console.clear_console()

# Create and start the HTTP server thread
http_server_thread = Thread(target=chrome_engine.start_chrome_engine)
http_server_thread.start()

obsidian_thread = Thread(target=obsidian_engine.obsidian_checker)
# obsidian_thread.start()

# Wait for both threads to finish
http_server_thread.join()
obsidian_thread.join()
