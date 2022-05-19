import sys
import tkinter as tk
import tkinter.ttk as ttk
import os

import jbs.database.database as db

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
database = scriptpath + "3D_Models.db"
print(database)

con = db.connect_database(database)

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

rows = db.get_all_models(con)
for row in rows:
    model_table.insert('', tk.END, values=row)

model_table.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

model_scroll.config(command=model_table.yview)

window.mainloop()

db.close_database(con)
