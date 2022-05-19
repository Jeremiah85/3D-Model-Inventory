import sys
import os

import jbs.database.database as db
import jbs.gui.gui as gui

def main():
    scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    database = scriptpath + "3D_Models.db"
    print(database)

    con = db.connect_database(database)

    #window = tk.Tk()
    #window.title("3D Models")
    app = gui.Window(con)
    #app.mainloop()
    app.root.mainloop()
    db.close_database(con)

if __name__ == "__main__":
    main()
