import tkinter as tk
import tkinter.ttk as ttk
import jbs.database.database as db
import jbs.model.model as mdl


class Window:
    def __init__(self, con):
        self.con = con
        self.root = tk.Tk()
        self.root.title("3D Models")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=tk.YES)

        # Create and populate Model tab
        #----------------------------------------------------------------------------------------------------
        self.model_frame = tk.Frame(self.tabs)
        self.model_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        # Fill results table
        self.model_display_frame = tk.LabelFrame(self.model_frame, text="Models")
        self.model_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.models = db.get_all_models(self.con)
        self.model_table = Table(self.model_display_frame, self.models)

        # Fill Model search section
        self.model_search_frame = tk.LabelFrame(self.model_frame, text="Search Models")
        self.model_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)
        self.model_search_options = ["Model_Name", "Set_Name", "Source_Note"]
        self.model_search_textbox = TextBox(self.model_search_frame, tk.LEFT, tk.W)
        self.model_search_selected = tk.StringVar()

        self.model_search_combobox = tk.OptionMenu(self.model_search_frame, self.model_search_selected, "Please select an option", *self.model_search_options)
        self.model_search_combobox.pack(side=tk.LEFT, anchor=tk.W)
        self.model_search_button = tk.Button(self.model_search_frame, text="Search", command=lambda: self.search_model())
        self.model_search_button.pack(padx=2, pady=2, side=tk.LEFT, anchor=tk.W)

        # Fill add model section
        self.model_newitem_frame = tk.LabelFrame(self.model_frame, text="Add Model")
        self.model_newitem_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.model_name_label = tk.Label(self.model_newitem_frame, text="Name")
        self.model_name_label.pack(side=tk.LEFT, anchor=tk.W)
        self.model_name_textbox = TextBox(self.model_newitem_frame, tk.LEFT, tk.W)

        self.model_set_label = tk.Label(self.model_newitem_frame, text="Set")
        self.model_set_label.pack(side=tk.LEFT, anchor=tk.W)
        self.model_set_textbox = TextBox(self.model_newitem_frame, tk.LEFT, tk.W)

        self.model_artist_label = tk.Label(self.model_newitem_frame, text="Artist")
        self.model_artist_label.pack(side=tk.LEFT, anchor=tk.W)
        self.artist_selection_obj = db.get_all_artists(con)
        self.model_artist_dropdown = DropdownBox(self.model_newitem_frame, self.artist_selection_obj, tk.LEFT, tk.W)

        self.model_source_label = tk.Label(self.model_newitem_frame, text="Source")
        self.model_source_label.pack(side=tk.LEFT, anchor=tk.W)
        self.source_selection_obj = db.get_all_artists(con)
        self.model_source_dropdown = DropdownBox(self.model_newitem_frame, self.source_selection_obj, tk.LEFT, tk.W)

        self.model_source_note_label = tk.Label(self.model_newitem_frame, text="Source Note")
        self.model_source_note_label.pack(side=tk.LEFT, anchor=tk.W)
        self.model_source_note_textbox = TextBox(self.model_newitem_frame, tk.LEFT, tk.W)

        self.model_supports_chkbox = CheckBox(self.model_newitem_frame, "Supports", tk.LEFT, tk.W)

        self.model_format_label = tk.Label(self.model_newitem_frame, text="Format")
        self.model_format_label.pack(side=tk.LEFT, anchor=tk.W)
        self.model_format_textbox = TextBox(self.model_newitem_frame, tk.LEFT, tk.W)

        self.model_printed_chkbox = CheckBox(self.model_newitem_frame, "Printed", tk.LEFT, tk.W)

        self.model_submit_button = tk.Button(self.model_newitem_frame, text="Submit", command=lambda: self.add_model())
        self.model_submit_button.pack(padx=2, pady=2, side=tk.LEFT, anchor=tk.W)

        self.tabs.add(self.model_frame, text="Models")
        #---------------------------------------------------------------------------------------------------- 

        # Create and populate Artist tab
        #----------------------------------------------------------------------------------------------------
        self.artist_frame = tk.Frame(self.tabs)
        self.artist_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        # Fill results table
        self.artist_display_frame = tk.LabelFrame(self.artist_frame, text="Artists")
        self.artist_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.artists = db.get_all_artists(self.con)
        self.artist_table = Table(self.artist_display_frame, self.artists)

        # Fill Artist search section
        self.artist_search_frame = tk.LabelFrame(self.artist_frame, text="Search Artists")
        self.artist_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)

        self.artist_search_textbox = TextBox(self.artist_search_frame, tk.LEFT, tk.W)
        self.artist_search_button = tk.Button(self.artist_search_frame, text="Search", command=lambda: self.search_artist())
        self.artist_search_button.pack(padx=2, pady=2, side=tk.LEFT, anchor=tk.W)

        # Fill Add Artist section
        self.artist_newitem_frame = tk.LabelFrame(self.artist_frame, text="Add Artist")
        self.artist_newitem_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)

        self.artist_name_label = tk.Label(self.artist_newitem_frame, text="Name")
        self.artist_name_label.pack(side=tk.TOP, anchor=tk.W)
        self.artist_name_textbox = TextBox(self.artist_newitem_frame, tk.TOP, tk.W)

        self.artist_website_label = tk.Label(self.artist_newitem_frame, text="Website")
        self.artist_website_label.pack(side=tk.TOP,anchor=tk.W)
        self.artist_website_textbox = TextBox(self.artist_newitem_frame, tk.TOP, tk.W)

        self.artist_email_label = tk.Label(self.artist_newitem_frame, text="Email")
        self.artist_email_label.pack(side=tk.TOP, anchor=tk.W)
        self.artist_email_textbox = TextBox(self.artist_newitem_frame, tk.TOP, tk.W)

        self.artist_folder_label = tk.Label(self.artist_newitem_frame, text="Folder")
        self.artist_folder_label.pack(side=tk.TOP,anchor=tk.W)
        self.artist_folder_textbox = TextBox(self.artist_newitem_frame, tk.TOP, tk.W)

        self.artist_submit_button = tk.Button(self.artist_newitem_frame, text="Submit", command=lambda: self.add_artist())
        self.artist_submit_button.pack(padx=2, pady=2, side=tk.TOP, anchor=tk.W)

        self.tabs.add(self.artist_frame, text="Artists")
        #----------------------------------------------------------------------------------------------------

        # Create and populate Source tab
        #----------------------------------------------------------------------------------------------------
        self.source_frame = tk.Frame(self.tabs)
        self.source_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        # Fill results table
        self.source_display_frame = tk.LabelFrame(self.source_frame, text="Sources")
        self.source_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.sources = db.get_all_sources(self.con)
        self.sources_table = Table(self.source_display_frame, self.sources)

        # Fill Source Search section
        self.source_search_frame = tk.LabelFrame(self.source_frame, text="Search Sources")
        self.source_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)

        self.source_search_textbox = TextBox(self.source_search_frame, tk.LEFT, tk.W)
        self.source_search_button = tk.Button(self.source_search_frame, text="Search", command=lambda: self.search_source())
        self.source_search_button.pack(padx=2, pady=2, side=tk.LEFT, anchor=tk.W)

        # Fill Add Source section
        self.source_newitem_frame = tk.LabelFrame(self.source_frame, text="Add Source")
        self.source_newitem_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)

        self.source_name_label = tk.Label(self.source_newitem_frame, text="Name")
        self.source_name_label.pack(side=tk.TOP, anchor=tk.W)
        self.source_name_textbox = TextBox(self.source_newitem_frame, tk.TOP, tk.W)

        self.source_website_label = tk.Label(self.source_newitem_frame, text="Website")
        self.source_website_label.pack(side=tk.TOP,anchor=tk.W)
        self.source_website_textbox = TextBox(self.source_newitem_frame, tk.TOP, tk.W)

        self.source_submit_button = tk.Button(self.source_newitem_frame, text="Submit", command=lambda: self.add_source())
        self.source_submit_button.pack(padx=2, pady=2, side=tk.TOP, anchor=tk.W)

        self.tabs.add(self.source_frame, text="Sources")
        #----------------------------------------------------------------------------------------------------

    def refresh_tables(self, con):
        # TODO: add code to refresh dropdown boxes
        self.connection = con
        self.updated_model_table = db.get_all_models(self.connection)
        self.updated_artist_table = db.get_all_artists(self.connection)
        self.updated_source_table = db.get_all_sources(self.connection)

        self.model_table.refresh_table(self.updated_model_table)
        self.artist_table.refresh_table(self.updated_artist_table)
        self.sources_table.refresh_table(self.updated_source_table)

    def add_model(self):
        self.new_model_entry = []
        self.new_model_entry.append(self.model_name_textbox.get_text())
        self.model_name_textbox.clear_text()
        self.new_model_entry.append(self.model_set_textbox.get_text())
        self.new_model_entry.append(self.model_artist_dropdown.get_selection())
        self.new_model_entry.append(self.model_source_dropdown.get_selection())
        self.new_model_entry.append(self.model_source_note_textbox.get_text())
        self.new_model_entry.append(self.model_supports_chkbox.get_selection())
        self.new_model_entry.append(self.model_format_textbox.get_text())
        self.new_model_entry.append("") # Adds a placeholder because a new model does not need to insert a folder
        self.new_model_entry.append(self.model_printed_chkbox.get_selection())

        self.new_model = mdl.Model(self.new_model_entry)
        db.add_model(self.con, self.new_model)

    def add_artist(self):
        self.new_artist_entry = []
        self.new_artist_entry.append(self.artist_name_textbox.get_text())
        self.artist_name_textbox.clear_text()
        self.new_source_entry.append(self.artist_website_textbox.get_text())
        self.artist_website_textbox.clear_text()
        self.new_source_entry.append(self.artist_email_textbox.get_text())
        self.artist_email_textbox.clear_text()
        self.new_source_entry.append(self.artist_folder_textbox.get_text())
        self.artist_folder_textbox.clear_text()

        self.new_artist = mdl.Artist(self.new_artist_entry)
        db.add_artist(self.con, self.new_artist)

    def add_source(self):
        self.new_source_entry = []
        self.new_source_entry.append(self.source_name_textbox.get_text())
        self.source_name_textbox.clear_text()
        self.new_source_entry.append(self.source_website_textbox.get_text())
        self.source_website_textbox.clear_text()

        self.new_source = mdl.Source(self.new_source_entry)
        db.add_source(self.con, self.new_source)

    def search_models(self, search_column):
        # TODO: create search model method
        self = search_column

    def search_artist(self):
        # TODO: create search_artist method
        pass

    def search_source(self):
        # TODO: create search_source method
        pass


class Table:
    def __init__(self, frame, input_obj):
        self.frame = frame
        self.input_obj = input_obj
        self.scroll = tk.Scrollbar(self.frame)
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

    def refresh_table(self, input_obj):
        self.input_obj = input_obj
        self.clear_table()
        self.add_rows(self.input_obj)


class TextBox:
    def __init__(self, frame, side, anchor):
        self.frame = frame
        self.side = side
        self.anchor = anchor

        self.text_box = tk.Text(self.frame, height=1, width=30)
        self.text_box.pack(padx=2, pady=2, side=self.side, anchor=self.anchor)

    def get_text(self):
        self.input = self.text_box.get(1.0, tk.END+"-1c")
        return self.input

    def clear_text(self):
        self.text_box.delete(1.0, tk.END+"-1c")


class DropdownBox:
    # TODO: Add refresh data method
    def __init__(self, frame, input_obj, side, anchor):
        self.frame = frame
        self.side = side
        self.anchor = anchor
        self.input_obj = input_obj
        self.default = "Please select from list"
        self.var = tk.StringVar(value=self.default)
        self.options = []

        for self.item in self.input_obj:
            self.options.append(self.item.name)

        self.dropdown = tk.OptionMenu(self.frame, self.var, self.default, *self.options)
        self.dropdown.pack(padx=2, pady=2, side=self.side, anchor=self.anchor)

    def get_selection(self):
        return self.var.get()

    def reset_selection(self):
        self.var.set(self.default)


class CheckBox:
    def __init__(self, frame, text, side, anchor):
        self.frame = frame
        self.side = side
        self.anchor = anchor
        self.text = text
        self.var = tk.BooleanVar()

        self.checkbox = tk.Checkbutton(self.frame, text=self.text, onvalue=tk.TRUE, offvalue=tk.FALSE, variable=self.var)
        self.checkbox.pack(padx=2, pady=2, side=self.side, anchor=self.anchor)

    def get_selection(self):
        return self.var.get()

    def clear_selection(self):
        self.checkbox.deselect()
