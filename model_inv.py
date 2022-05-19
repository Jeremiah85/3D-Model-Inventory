import sys
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import os

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
database = scriptpath + "3D_Models.db"
print(database)

def get_models(db):
    
    con = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        
        cur.execute("SELECT Model_Name, Set_Name, Artist_Name, Source_Name "
                    "FROM tblModel AS m "
                    "INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID "
                    "INNER JOIN tblSource AS s ON m.Source = s.Source_ID;"
                    )

        return cur.fetchall()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)

    finally:
        if con:
            con.close()


window = tk.Tk()
window.title("3D Models")

model_frame = tk.Frame(window)
model_frame.pack(fill=tk.BOTH, expand=tk.YES)

model_scroll = tk.Scrollbar(model_frame)
model_scroll.pack(side=tk.RIGHT, fill=tk.Y)

model_table = ttk.Treeview(model_frame, yscroll=model_scroll.set)
model_table['columns'] = ('Model', 'Set', 'Artist', 'Source')
model_table.column("#0", width=0, stretch=tk.NO)
model_table.column("Model", anchor=tk.W, width=80)
model_table.column("Set", anchor=tk.W, width=80)
model_table.column("Artist", anchor=tk.W, width=80)
model_table.column("Source", anchor=tk.W, width=80)

model_table.heading("#0", text="", anchor=tk.CENTER)
model_table.heading("Model", text="Model", anchor=tk.CENTER)
model_table.heading("Set", text="Set", anchor=tk.CENTER)
model_table.heading("Artist", text="Artist", anchor=tk.CENTER)
model_table.heading("Source", text="Source", anchor=tk.CENTER)

rows = get_models(database)
for row in rows:
    model_table.insert('', tk.END, values=row)

model_table.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

model_scroll.config(command=model_table.yview)

window.mainloop()
