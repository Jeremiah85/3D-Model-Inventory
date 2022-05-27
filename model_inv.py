import sys
import os

import jbs.database.database_utils as db
import jbs.gui as gui

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
database = scriptpath + "3D_Models.db"
sql_schema_new = scriptpath + r'sql\empty_database.sql'

def main():
    if os.path.exists(database):
        con = db.connect_database(database)
    else:
        con = db.connect_database(database)
        db.modify_database_schema(con, sql_schema_new)
        
    app = gui.Window(con)
    app.root.mainloop()

    db.close_database(con)

if __name__ == '__main__':
    main()
