import tkinter as tk
import tkinter.ttk as ttk

import jbs.database.database as db

class Window:
    def __init__(self, con):
        self.con = con
        self.root = tk.Tk()
        self.root.title("3D Models")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.scroll = tk.Scrollbar(self.frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(self.frame, yscroll=self.scroll.set)
        self.table['columns'] = ('Model', 'Set', 'Artist', 'Source')
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("Model", anchor=tk.W, width=80)
        self.table.column("Set", anchor=tk.W, width=80)
        self.table.column("Artist", anchor=tk.W, width=80)
        self.table.column("Source", anchor=tk.W, width=80)

        self.table.heading("#0", text="", anchor=tk.CENTER)
        self.table.heading("Model", text="Model", anchor=tk.CENTER)
        self.table.heading("Set", text="Set", anchor=tk.CENTER)
        self.table.heading("Artist", text="Artist", anchor=tk.CENTER)
        self.table.heading("Source", text="Source", anchor=tk.CENTER)

        rows = db.get_all_models(self.con)
        for row in rows:
            self.table.insert('', tk.END, values=row)

        self.table.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.scroll.config(command=self.table.yview)
