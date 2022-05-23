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

        # TODO: write logic to refresh tables
        # TODO: create ui for data entry
        
        # Create and populate Model tab
        self.model_frame = tk.Frame(self.tabs)
        self.model_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.model_search_frame = tk.LabelFrame(self.model_frame, text="Search Models")
        self.model_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.model_newitem_frame = tk.LabelFrame(self.model_frame, text="Add Model")
        self.model_newitem_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.model_display_frame = tk.LabelFrame(self.model_frame, text="Models")
        self.model_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.models = db.get_all_models(self.con)
        model_table = Table(self.model_display_frame, self.models)

        self.tabs.add(self.model_frame, text="Models")

        # Create and populate Artist tab
        self.artist_frame = tk.Frame(self.tabs)
        self.artist_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.artist_search_frame = tk.LabelFrame(self.artist_frame, text="Search Artists")
        self.artist_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.artist_newitem_frame = tk.LabelFrame(self.artist_frame, text="Add Artist")
        self.artist_newitem_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.artist_display_frame = tk.LabelFrame(self.artist_frame, text="Artists")
        self.artist_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.artists = db.get_all_artists(self.con)
        artist_table = Table(self.artist_display_frame, self.artists)

        self.tabs.add(self.artist_frame, text="Artists")

        # Create and populate Source tab
        self.source_frame = tk.Frame(self.tabs)
        self.source_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.source_search_frame = tk.LabelFrame(self.source_frame, text="Search Sources")
        self.source_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.source_newitem_frame = tk.LabelFrame(self.source_frame, text="Add Source")
        self.source_newitem_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.source_display_frame = tk.LabelFrame(self.source_frame, text="Sources")
        self.source_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        self.sources = db.get_all_sources(self.con)
        sources_table = Table(self.source_display_frame, self.sources)

        self.tabs.add(self.source_frame, text="Sources")


class Table:
    def __init__(self, frame, input_obj):
        self.input_obj = input_obj
        self.scroll = tk.Scrollbar(frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(frame, yscroll=self.scroll.set)
        self.table.pack(padx=2, pady=2, expand=True, fill=tk.BOTH)
        self.scroll.config(command=self.table.yview)

        self.add_rows(self.input_obj)

    def add_rows(self, input_obj):
        self.input_obj = input_obj
        self.column_names_temp = vars(input_obj[0])
        self.column_names = self.column_names_temp.keys()

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

    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
