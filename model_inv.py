import sys
import tkinter as tk
import tkinter.ttk as ttk
import os

import jbs.database.database as db
import jbs.gui.gui as gui

def main():
    scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    database = scriptpath + "3D_Models.db"
    print(database)

    con = db.connect_database(database)

    window = tk.Tk()
    window.title("3D Models")
    app = gui.Window(window,con)
    window.mainloop()

    db.close_database(con)

if __name__ == "__main__":
    main()
