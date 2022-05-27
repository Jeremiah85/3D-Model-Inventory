# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import tkinter as tk
import tkinter.ttk as ttk

import jbs.database.database_queries as dbqueries
import jbs.inventory as inv


class Window:
    """Creates and populates the main program window.

    An instance of this class creates the main program window along with it's
    tabs, frames, and form widgets. This class receives a SQLite3 database
    connection.
    """
    def __init__(self, connection):
        """Initializes the Window class.

        Creates three tabs: Models, Artists, and Sources, each with a search,
        add, and display section. The database connection is used to populate
        various UI elements.
        """
        self.connection = connection
        self.root = tk.Tk()
        self.root.title("3D Models")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=tk.YES)

        # Create and populate Model tab -------------------------------------------------------------------------------
        self.model_frame = tk.Frame(self.tabs)
        self.model_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        # Fill results table
        self.model_display_frame = tk.LabelFrame(self.model_frame, text="Models")
        self.model_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.models = dbqueries.get_all_models(self.connection)
        self.model_table = Table(self.model_display_frame, self.models)

        # Fill Model search section
        self.model_search_frame = tk.LabelFrame(self.model_frame, text="Search Models")
        self.model_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)
        self.model_search_options = ["Model_Name", "Set_Name", "Source_Note"]
        self.model_search_textbox = TextBox(self.model_search_frame, tk.LEFT, tk.W)
        self.model_search_selected = tk.StringVar()

        self.model_search_combobox = tk.OptionMenu(
            self.model_search_frame,
            self.model_search_selected,
            *self.model_search_options
            )
        self.model_search_combobox.pack(side=tk.LEFT, anchor=tk.W)
        self.model_search_button = tk.Button(
            self.model_search_frame,
            text="Search",
            command=lambda: self.search_models()
            )
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
        self.artist_selection_obj = dbqueries.get_all_artists(self.connection)
        self.model_artist_dropdown = DropdownBox(
            self.model_newitem_frame,
            self.artist_selection_obj,
            tk.LEFT,
            tk.W
            )

        self.model_source_label = tk.Label(self.model_newitem_frame, text="Source")
        self.model_source_label.pack(side=tk.LEFT, anchor=tk.W)
        self.source_selection_obj = dbqueries.get_all_artists(self.connection)
        self.model_source_dropdown = DropdownBox(
            self.model_newitem_frame,
            self.source_selection_obj,
            tk.LEFT,
            tk.W
            )

        self.model_source_note_label = tk.Label(self.model_newitem_frame, text="Source Note")
        self.model_source_note_label.pack(side=tk.LEFT, anchor=tk.W)
        self.model_source_note_textbox = TextBox(self.model_newitem_frame, tk.LEFT, tk.W)

        self.model_supports_chkbox = CheckBox(self.model_newitem_frame, "Supports", tk.LEFT, tk.W)

        self.model_format_label = tk.Label(self.model_newitem_frame, text="Format")
        self.model_format_label.pack(side=tk.LEFT, anchor=tk.W)
        self.model_format_textbox = TextBox(self.model_newitem_frame, tk.LEFT, tk.W)

        self.model_printed_chkbox = CheckBox(self.model_newitem_frame, "Printed", tk.LEFT, tk.W)

        self.model_submit_button = tk.Button(
            self.model_newitem_frame,
            text="Submit",
            command=lambda: self.add_model()
            )
        self.model_submit_button.pack(padx=2, pady=2, side=tk.LEFT, anchor=tk.W)

        self.tabs.add(self.model_frame, text="Models")
        #--------------------------------------------------------------------------------------------------------------

        # Create and populate Artist tab ------------------------------------------------------------------------------
        self.artist_frame = tk.Frame(self.tabs)
        self.artist_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        # Fill results table
        self.artist_display_frame = tk.LabelFrame(self.artist_frame, text="Artists")
        self.artist_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.artists = dbqueries.get_all_artists(self.connection)
        self.artist_table = Table(self.artist_display_frame, self.artists)

        # Fill Artist search section
        self.artist_search_frame = tk.LabelFrame(self.artist_frame, text="Search Artists")
        self.artist_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)

        self.artist_search_textbox = TextBox(self.artist_search_frame, tk.LEFT, tk.W)
        self.artist_search_button = tk.Button(
            self.artist_search_frame,
            text="Search",
            command=lambda: self.search_artist())
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

        self.artist_submit_button = tk.Button(
            self.artist_newitem_frame,
            text="Submit",
            command=lambda: self.add_artist()
            )
        self.artist_submit_button.pack(padx=2, pady=2, side=tk.TOP, anchor=tk.W)

        self.tabs.add(self.artist_frame, text="Artists")
        #---------------------------------------------------------------------------------------------------------------

        # Create and populate Source tab -------------------------------------------------------------------------------
        self.source_frame = tk.Frame(self.tabs)
        self.source_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)

        # Fill results table
        self.source_display_frame = tk.LabelFrame(self.source_frame, text="Sources")
        self.source_display_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.BOTTOM)

        self.sources = dbqueries.get_all_sources(self.connection)
        self.sources_table = Table(self.source_display_frame, self.sources)

        # Fill Source Search section
        self.source_search_frame = tk.LabelFrame(self.source_frame, text="Search Sources")
        self.source_search_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES, side=tk.LEFT)

        self.source_search_textbox = TextBox(self.source_search_frame, tk.LEFT, tk.W)
        self.source_search_button = tk.Button(
            self.source_search_frame,
            text="Search",
            command=lambda: self.search_source()
            )
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

        self.source_submit_button = tk.Button(
            self.source_newitem_frame,
            text="Submit",
            command=lambda: self.add_source()
            )
        self.source_submit_button.pack(padx=2, pady=2, side=tk.TOP, anchor=tk.W)

        self.tabs.add(self.source_frame, text="Sources")
        #--------------------------------------------------------------------------------------------------------------

    def refresh_tables(self):
        """Replaces the tables and dropdowns with new data from the database.

        Pulls the latest data from the database and repopulates the three
        tables and the two model dropdowns.
        """
        self.updated_model_table = dbqueries.get_all_models(self.connection)
        self.updated_artist_table = dbqueries.get_all_artists(self.connection)
        self.updated_source_table = dbqueries.get_all_sources(self.connection)

        self.model_table.refresh_table(self.updated_model_table)
        self.artist_table.refresh_table(self.updated_artist_table)
        self.sources_table.refresh_table(self.updated_source_table)

        self.refreshed_artists = dbqueries.get_all_artists(self.connection)
        self.model_artist_dropdown.refresh_options(self.refreshed_artists)
        self.refreshed_sources = dbqueries.get_all_sources(self.connection)
        self.model_source_dropdown.refresh_options(self.refreshed_sources)

    def add_model(self):
        """Adds a new model to the database.

        Gathers the data that the user entered into the add model form and 
        creates a model object to be inserted into the database. 
        After inserting the model, it refreshes the tables and dropdowns so 
        that they reflect the new data.
        """
        self.new_model_entry = []
        self.new_model_entry.append(self.model_name_textbox.get_text())
        self.model_name_textbox.clear_text()
        self.new_model_entry.append(self.model_set_textbox.get_text())
        self.new_model_entry.append(self.model_artist_dropdown.get_selection())
        self.new_model_entry.append(self.model_source_dropdown.get_selection())
        self.new_model_entry.append(self.model_source_note_textbox.get_text())
        self.new_model_entry.append(self.model_supports_chkbox.get_selection())
        self.new_model_entry.append(self.model_format_textbox.get_text())
        # Adds a placeholder because a folder is not needed
        self.new_model_entry.append('')
        self.new_model_entry.append(self.model_printed_chkbox.get_selection())

        self.new_model = inv.Model(self.new_model_entry)
        dbqueries.add_model(self.connection, self.new_model)
        self.refresh_tables()

    def add_artist(self):
        """Adds a new artist to the database.

        Gathers the data that the user entered into the add artist form and 
        creates an artist object to be inserted into the database. 
        After inserting the artist, it refreshes the tables and dropdowns so 
        that they reflect the new data.
        """
        self.new_artist_entry = []
        self.new_artist_entry.append(self.artist_name_textbox.get_text())
        self.artist_name_textbox.clear_text()
        self.new_source_entry.append(self.artist_website_textbox.get_text())
        self.artist_website_textbox.clear_text()
        self.new_source_entry.append(self.artist_email_textbox.get_text())
        self.artist_email_textbox.clear_text()
        self.new_source_entry.append(self.artist_folder_textbox.get_text())
        self.artist_folder_textbox.clear_text()

        self.new_artist = inv.Artist(self.new_artist_entry)
        dbqueries.add_artist(self.connection, self.new_artist)
        self.refresh_tables()

    def add_source(self):
        """Adds a new source to the database.

        Gathers the data that the user entered into the add source form and 
        creates a source object to be inserted into the database. 
        After inserting the source, it refreshes the tables and dropdown so 
        that they reflect the new data.
        """
        self.new_source_entry = []
        self.new_source_entry.append(self.source_name_textbox.get_text())
        self.source_name_textbox.clear_text()
        self.new_source_entry.append(self.source_website_textbox.get_text())
        self.source_website_textbox.clear_text()

        self.new_source = inv.Source(self.new_source_entry)
        dbqueries.add_source(self.connection, self.new_source)
        self.refresh_tables()

    def search_models(self):
        """Searches the database for models matching a search term.

        Gathers the user's search term and selected field to search and returns
        the matching rows as a model object then refreshes the model table so 
        that it will reflect the newly entered data.

        Returns:
            A list of model objects matching the query
        """
        self.model_search_term = self.model_search_textbox.get_text()
        self.model_search_textbox.clear_text()
        self.model_search_field = self.model_search_selected.get()

        self.model_results = dbqueries.search_model(
            self.connection,
            self.model_search_field,
            self.model_search_term
            )
        self.model_table.refresh_table(self.model_results)
        
    def search_artist(self):
        """Searches the database for artists matching a search term.

        Gathers the user's search term and returns the matching rows as an
        artist object then refreshes the artist table so that it will reflect
        the newly entered data.

        Returns:
            A list of artist objects matching the query
        """
        self.artist_search_term = self.artist_search_textbox.get_text()
        self.artist_search_textbox.clear_text()

        self.artist_results = dbqueries.search_artist(self.connection, self.artist_search_term)
        self.artist_table.refresh_table(self.artist_results)

    def search_source(self):
        """Searches the database for sources matching a search term.

        Gathers the user's search term and returns the matching rows as a
        source object then refreshes the sources table so that it will reflect
        the newly entered data.

        Returns:
            A list of source objects matching the query
        """
        self.source_search_term = self.source_search_textbox.get_text()
        self.source_search_textbox.clear_text()

        self.search_results = dbqueries.search_source(self.connection, self.source_search_term)
        self.sources_table.refresh_table(self.search_results)

class Table:
    """Creates a table from the passed objects in the specified frame.

    This class takes a list of one or more input objects and uses that data to
    create a table in the specified frame. The object's attribute names become
    the header names and each object is added as a row to the new table. 
    Methods are also provided to clear the table and to refresh the table with
    new data.
    """
    def __init__(self, frame, input_obj):
        """Creates an empty table.

        Creates an empty table in the specified frame using data from an input
        object. 

        Args:
            frame: The frame that the table should be created in.
            input_obj: The object used to populate the table.
        """
        self.frame = frame
        self.input_obj = input_obj
        self.scroll = tk.Scrollbar(self.frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(frame, yscroll=self.scroll.set)
        self.table.pack(padx=2, pady=2, expand=True, fill=tk.BOTH)
        self.scroll.config(command=self.table.yview)

        self.add_rows(self.input_obj)

    def add_rows(self, input_obj):
        """Adds rows to the table from a supplied object.

        Takes an list of objects and uses its attributes to create the headers
        and enters one object per row in the table.

        Args:
            input_obj: A list of model, artist, or source objects.
        """
        self.input_obj = input_obj
        self.column_names_temp = vars(input_obj[0])
        self.column_names = self.column_names_temp.keys()

        self.columns = []
        for self.name in self.column_names:
            self.columns.append(self.name)

        self.table['columns'] = self.columns

        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.heading('#0', text="", anchor=tk.W)
        for self.heading in self.column_names:
            self.table.column(self.heading, anchor=tk.W, width=80)
            self.table.heading(self.heading, text=self.heading.capitalize(), anchor=tk.W)

        for self.row in self.input_obj:
            self.table.insert('', tk.END, values=(self.row.to_list()))

    def clear_table(self):
        """Clears the data from the table."""
        for item in self.table.get_children():
            self.table.delete(item)

    def refresh_table(self, input_obj):
        """Replaces the data in the table.

        Takes the data from the input object and repopulates the table with
        that data.

        Args:
            input_obj: A list of model, artist, or source objects.
        """
        self.input_obj = input_obj
        self.clear_table()
        self.add_rows(self.input_obj)


class TextBox:
    """ Creates a text entry box.

    Creates a text entry box in the specified frame with the specified side and
    anchor.
    """
    def __init__(self, frame, side, anchor):
        """Inits the new text entry box.

        Sets the text box's size side and anchor position.

        Args:
            frame: The frame that the text box will be created in.
            side: Accepts a tkinter side
            anchor: Accepts a tkinter anchor location
        """
        self.frame = frame
        self.side = side
        self.anchor = anchor

        self.text_box = tk.Text(self.frame, height=1, width=30)
        self.text_box.pack(padx=2, pady=2, side=self.side, anchor=self.anchor)

    def get_text(self):
        """Retrieves the text from the text box.

        Returns:
            A string containing the text entered in the text box.
        """
        self.input = self.text_box.get(1.0, tk.END+'-1c')
        return self.input

    def clear_text(self):
        """Removes the text from the text box."""
        self.text_box.delete(1.0, tk.END+'-1c')


class DropdownBox:
    """ Creates a dropdown box.

    Creates a dropdown box in the specified frame with the specified side and
    anchor.
    """
    def __init__(self, frame, input_obj, side, anchor):
        """Inits the new text entry box.

        Sets the text box's size, side, and anchor position.

        Args:
            frame: The frame that the text box will be created in.
            side: Accepts a tkinter side
            anchor: Accepts a tkinter anchor location
        """
        self.frame = frame
        self.side = side
        self.anchor = anchor
        self.input_obj = input_obj
        self.var = tk.StringVar()
        self.options = []

        for self.item in self.input_obj:
            self.options.append(self.item.name)

        self.dropdown = tk.OptionMenu(self.frame, self.var, None, *self.options)
        self.dropdown.pack(padx=2, pady=2, side=self.side, anchor=self.anchor)

    def get_selection(self):
        """Gets the selected item.

        Retrieves the selected item from the dropdown box.

        Returns:
            A string containing the user's selection.
        """
        return self.var.get()

    def reset_selection(self):
        """Resets the dropdown box back to the default selection."""
        self.var.set(self.default)

    def refresh_options(self, input):
        """Replaces the data in the dropdown.

        Takes the data from the input object and repopulates the dropdown with
        that data.

        Args:
            input: A list of artist or source objects.
        """
        self.input_obj = input
        self.dropdown['menu'].delete(0, tk.END)
        for item in self.input_obj:
            self.dropdown['menu'].add_command(
                label=item.name,
                command=lambda value=item.name: self.var.set(value)
                )


class CheckBox:
    """ Creates a check box.

    Creates a dropdown box in the specified frame with the specified side and
    anchor.
    """
    def __init__(self, frame, text, side, anchor):
        """Inits the new  checkbox.

        Sets the checkbox's size, side, and anchor position.

        Args:
            frame: The frame that the text box will be created in.
            text: The text for the builtin label.
            side: Accepts a tkinter side.
            anchor: Accepts a tkinter anchor location.
        """
        self.frame = frame
        self.side = side
        self.anchor = anchor
        self.text = text
        self.var = tk.BooleanVar()

        self.checkbox = tk.Checkbutton(
            self.frame, 
            text=self.text,
            onvalue=tk.TRUE,
            offvalue=tk.FALSE,
            variable=self.var
            )
        self.checkbox.pack(padx=2, pady=2, side=self.side, anchor=self.anchor)

    def get_selection(self):
        """Gets the selected item.

        Retrieves the state of the checkbox.

        Returns:
            A boolean with the selected state of the checkbox.
        """
        return self.var.get()

    def clear_selection(self):
        """Reset the checkbox to the initial state of False"""
        self.checkbox.deselect()
