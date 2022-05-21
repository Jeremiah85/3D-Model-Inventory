import tkinter as tk
import tkinter.ttk as ttk

import jbs.database.database as db

class Window:
    def __init__(self, con):
        # TODO: Add TTK Notebook for tabs
        self.con = con
        self.root = tk.Tk()
        self.root.title("3D Models")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=tk.YES)

        # TODO: Separate table creation into its own method
        self.scroll = tk.Scrollbar(self.frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(self.frame, yscroll=self.scroll.set)
        self.table['columns'] = ('Model', 'Set', 'Artist', 'Source', 'Source_Note', 'Supports', 'Format', 'Artist_Folder', 'Printed')
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("Model", anchor=tk.W, width=80)
        self.table.column("Set", anchor=tk.W, width=80)
        self.table.column("Artist", anchor=tk.W, width=80)
        self.table.column("Source", anchor=tk.W, width=80)
        self.table.column("Source_Note", anchor=tk.W, width=80)
        self.table.column("Supports", anchor=tk.W, width=80)
        self.table.column("Format", anchor=tk.W, width=80)
        self.table.column("Artist_Folder", anchor=tk.W, width=80)
        self.table.column("Printed", anchor=tk.W, width=80)

        self.table.heading("#0", text="", anchor=tk.CENTER)
        self.table.heading("Model", text="Model", anchor=tk.CENTER)
        self.table.heading("Set", text="Set", anchor=tk.CENTER)
        self.table.heading("Artist", text="Artist", anchor=tk.CENTER)
        self.table.heading("Source", text="Source", anchor=tk.CENTER)
        self.table.heading("Source_Note", text="Source Note", anchor=tk.CENTER)
        self.table.heading("Supports", text="Supports", anchor=tk.CENTER)
        self.table.heading("Format", text="Format", anchor=tk.CENTER)
        self.table.heading("Artist_Folder", text="Folder", anchor=tk.CENTER)
        self.table.heading("Printed", text="Printed", anchor=tk.CENTER)

        rows = db.get_all_models(self.con)
        for row in rows:
            self.table.insert('', tk.END, values=(row.to_list()))

        self.table.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.scroll.config(command=self.table.yview)

    def create_table(self, frame, **kargs):
        # TODO: Replace kargs with object
        # TODO: Extract one object to create columns and headings
        self.scroll = tk.Scrollbar(frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(frame, yscroll=self.scroll.set)

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.heading("#0", text="", anchor=tk.CENTER)
        # TODO: Add loop to create columns

        # TODO: Populate the table
