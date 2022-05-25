import sys
import os

import jbs.database.database as db
import jbs.gui as gui

def main():
    # This assumes that the database is in the same directory as the script.
    # TODO: Eventually I want to allow a json or xml or yaml file in the script
    # directory to explicitly define the database name and location with 
    # this as a fallback
    scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    database = scriptpath + "3D_Models.db"

    con = db.connect_database(database)

    app = gui.Window(con)
    app.root.mainloop()

    db.close_database(con)

if __name__ == '__main__':
    main()
