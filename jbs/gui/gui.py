import tkinter as tk
import tkinter.ttk as ttk

import jbs.database.database as db

class Window:
    def __init__(self, con):
        self.con = con
        self.root = tk.Tk()
        self.root.title("3D Models")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=tk.YES)

        # Create and populate Model tab
        self.model_frame = tk.LabelFrame(self.tabs, text="Results")
        self.model_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.models = db.get_all_models(self.con)
        self.create_table(self.model_frame, self.models)

        self.tabs.add(self.model_frame, text="Models")

        # Create and populate Artist tab
        self.artist_frame = tk.LabelFrame(self.tabs, text="Results")
        self.artist_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.artists = db.get_all_artists(self.con)
        self.create_table(self.artist_frame, self.artists)

        self.tabs.add(self.artist_frame, text="Artists")

        # Create and populate Source tab
        self.source_frame = tk.LabelFrame(self.tabs, text="Results")
        self.source_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.sources = db.get_all_sources(self.con)
        self.create_table(self.source_frame, self.sources)

        self.tabs.add(self.source_frame, text="Sources")

    def create_table(self, frame, input_obj):
        self.input_obj = input_obj
        self.column_names_temp = vars(input_obj[0])
        self.column_names = self.column_names_temp.keys()

        self.scroll = tk.Scrollbar(frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(frame, yscroll=self.scroll.set)

        self.columns = []
        for self.name in self.column_names:
            self.columns.append(self.name)

        self.table['columns'] = self.columns

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.heading("#0", text="", anchor=tk.CENTER)
        for self.heading in self.column_names:
            self.table.column(self.heading, anchor=tk.W, width=80)
            self.table.heading(self.heading, text=self.heading.capitalize(), anchor=tk.CENTER)

        for self.row in self.input_obj:
            self.table.insert('', tk.END, values=(self.row.to_list()))

        self.table.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.scroll.config(command=self.table.yview)
