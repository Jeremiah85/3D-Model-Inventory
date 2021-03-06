# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import csv
import logging
import pathlib
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import tkinter.ttk as ttk

import jbs.database.database_queries as dbqueries
import jbs.inventory as inv

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class Window:
    """Creates and populates the main program window.

    An instance of this class creates the main program window along 
    with it's tabs, frames, and form widgets. This class receives a
    SQLite3 database connection.
    """
    def __init__(self, connection):
        """Initializes the Window class.

        Creates three tabs: Models, Artists, and Sources, each with
        a search, add, and display section. The database connection
        is used to populate various UI elements.
        """
        self.factory = inv.ObjectFactory()
        self.connection = connection
        self.root = tk.Tk()
        self.root.title("3D Models")

        self.tabs = ttk.Notebook(master=self.root)
        self.tabs.pack(fill=tk.BOTH, expand=tk.YES)

        # Create and populate Model tab
        self.model_frame = tk.Frame(master=self.tabs)
        self.model_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)
        self.model_frame.columnconfigure(index=0, weight=1)
        self.model_frame.columnconfigure(index=1, weight=5)
        self.model_frame.rowconfigure(index=0, weight=1, uniform="model")
        self.model_frame.rowconfigure(index=1, weight=5, uniform="model")
        self.model_frame.rowconfigure(index=2, weight=1)

        # Fill results table
        self.model_display_frame = ttk.LabelFrame(
            master=self.model_frame,
            text="Models"
            )
        self.model_display_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.NSEW
            )

        logger.info("Populating model table")
        self.models = dbqueries.get_all_models(connection=self.connection)
        self.model_table = Table(
            frame=self.model_display_frame,
            input_obj=self.models
            )

        # Fill Model search section
        self.model_search_frame = ttk.LabelFrame(
            master=self.model_frame,
            text="Search Models"
            )
        self.model_search_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.model_search_frame.columnconfigure(index=0, weight=1)
        self.model_search_frame.rowconfigure(
            index=0,
            weight=1,
            uniform="model_search"
            )
        self.model_search_frame.rowconfigure(
            index=1,
            weight=1,
            uniform="model_search"
            )
        self.model_search_frame.rowconfigure(
            index=2,
            weight=1,
            uniform="model_search"
            )

        self.model_search_options = [
            "Model_Name",
            "Set_Name",
            "Source_Note",
            "Artist",
            "Source"
            ]
        self.model_search_textbox = TextBox(
            frame=self.model_search_frame,
            row=0,
            column=0,
            sticky=tk.S
            )
        self.model_search_selected = tk.StringVar()

        self.model_search_combobox = ttk.OptionMenu(
            self.model_search_frame,
            self.model_search_selected,
            self.model_search_options[0],
            *self.model_search_options
            )
        self.model_search_combobox.grid(row=1, column=0)
        self.model_search_button = ttk.Button(
            master=self.model_search_frame,
            text="Search",
            command=lambda: self.search_models()
            )
        self.model_search_button.grid(
            padx=2,
            pady=2,
            row=2,
            column=0,
            sticky=tk.N
            )

        def search_model_return(event):
            self.search_models()

        for self.widget in list(self.model_search_frame.children.values()):
            self.widget.bind(sequence='<Return>', func=search_model_return)

        # Fill add model section
        self.model_newitem_frame = ttk.LabelFrame(
            master=self.model_frame,
            text="Add Model"
            )
        self.model_newitem_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.model_newitem_frame.columnconfigure(index=0, weight=1)
        self.model_newitem_frame.columnconfigure(index=1, weight=1)
        self.model_newitem_frame.columnconfigure(index=2, weight=1)
        self.model_newitem_frame.columnconfigure(index=3, weight=1)
        self.model_newitem_frame.columnconfigure(index=4, weight=1)
        self.model_newitem_frame.columnconfigure(index=5, weight=1)
        self.model_newitem_frame.columnconfigure(index=6, weight=1)
        self.model_newitem_frame.columnconfigure(index=7, weight=1)
        self.model_newitem_frame.rowconfigure(
            index=0,
            weight=1,
            uniform="model_add"
            )
        self.model_newitem_frame.rowconfigure(
            index=1,
            weight=1,
            uniform="model_add"
            )
        self.model_newitem_frame.rowconfigure(
            index=2,
            weight=1,
            uniform="model_add"
            )

        self.model_name_label = ttk.Label(
            master=self.model_newitem_frame,
            text="Name"
            )
        self.model_name_label.grid(row=0, column=0, sticky=tk.SE)
        self.model_name_textbox = TextBox(
            frame=self.model_newitem_frame,
            row=0,
            column=1,
            sticky=tk.SW
            )

        self.model_set_label = ttk.Label(
            master=self.model_newitem_frame,
            text="Set"
            )
        self.model_set_label.grid(row=1, column=0, sticky=tk.NE)
        self.model_set_textbox = TextBox(
            frame=self.model_newitem_frame,
            row=1,
            column=1,
            sticky=tk.NW
            )

        self.model_artist_label = ttk.Label(
            master=self.model_newitem_frame,
            text="Artist"
            )
        self.model_artist_label.grid(row=0, column=2, sticky=tk.SE)
        logger.info("Populating artist dropdown for adding model")

        self.artist_selection_obj = dbqueries.get_all_artists(
            connection=self.connection
            )

        self.model_artist_dropdown = DropdownBox(
            frame=self.model_newitem_frame,
            input_obj=self.artist_selection_obj,
            row=0,
            column=3,
            sticky=tk.SW
            )

        self.model_source_label = ttk.Label(
            master=self.model_newitem_frame,
            text="Source"
            )
        self.model_source_label.grid(row=1, column=2, sticky=tk.NE)
        logger.info("Populating source dropdown for adding model")

        self.source_selection_obj = dbqueries.get_all_sources(
            connection=self.connection
            )

        self.model_source_dropdown = DropdownBox(
            frame=self.model_newitem_frame,
            input_obj=self.source_selection_obj,
            row=1,
            column=3,
            sticky=tk.NW
            )

        self.model_source_note_label = ttk.Label(
            master=self.model_newitem_frame,
            text="Source Note"
            )
        self.model_source_note_label.grid(row=0, column=4, sticky=tk.SE)
        self.model_source_note_textbox = TextBox(
            frame=self.model_newitem_frame,
            row=0,
            column=5,
            sticky=tk.SW
            )

        self.model_supports_chkbox = CheckBox(
            frame=self.model_newitem_frame,
            text="Supports",
            row=1,
            column=5,
            sticky=tk.N
            )

        self.model_format_label = ttk.Label(
            master=self.model_newitem_frame,
            text="Format"
            )
        self.model_format_label.grid(row=0, column=6, sticky=tk.SE)
        self.model_format_textbox = TextBox(
            frame=self.model_newitem_frame,
            row=0,
            column=7,
            sticky=tk.SW
            )

        self.model_printed_chkbox = CheckBox(
            frame=self.model_newitem_frame,
            text="Printed",
            row=1,
            column=7,
            sticky=tk.N
            )

        self.model_submit_button = ttk.Button(
            master=self.model_newitem_frame,
            text="Submit",
            command=lambda: self.add_model()
            )
        self.model_submit_button.grid(
            padx=2,
            pady=2,
            row=2,
            column=0,
            columnspan=8,
            sticky=tk.N
            )

        def add_model_return(event):
            self.add_model()

        for self.widget in list(self.model_newitem_frame.children.values()):
            self.widget.bind(sequence='<Return>', func=add_model_return)

        # Model Table commands
        self.model_tablecommand_frame = ttk.LabelFrame(
            master=self.model_frame,
            text="Table Commands"
            )
        self.model_tablecommand_frame.grid(
            row=2,
            column=0,
            sticky=tk.NSEW,
            columnspan=2
            )
        self.model_tablecommand_frame.columnconfigure(
            index=0,
            weight=1,
            uniform="model_tablecommand"
            )
        self.model_tablecommand_frame.columnconfigure(
            index=1,
            weight=1,
            uniform="model_tablecommand"
            )
        
        self.delete_model_button = ttk.Button(
            master=self.model_tablecommand_frame,
            text="Delete",
            command=lambda: self.delete_model()
            )
        self.delete_model_button.grid(
            column=0,
            row=0,
            sticky=tk.NW,
            padx=5,
            pady=5
            )

        self.export_models_button = ttk.Button(
            master=self.model_tablecommand_frame,
            text="Export",
            command=lambda: self.export_table(table=self.model_table)
            )
        self.export_models_button.grid(
            column=1,
            row=0,
            sticky=tk.NW,
            padx=5,
            pady=5
            )

        self.tabs.add(child=self.model_frame, text="Models")

        # Create and populate Artist tab
        self.artist_frame = tk.Frame(master=self.tabs)
        self.artist_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)
        self.artist_frame.columnconfigure(index=0, weight=1)
        self.artist_frame.columnconfigure(index=1, weight=5)
        self.artist_frame.rowconfigure(index=0, weight=1, uniform="artist")
        self.artist_frame.rowconfigure(index=1, weight=5, uniform="artist")
        self.artist_frame.rowconfigure(index=2, weight=1)

        # Fill results table
        self.artist_display_frame = ttk.LabelFrame(
            master=self.artist_frame,
            text="Artists"
            )
        self.artist_display_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.NSEW
            )

        logger.info("Populating artist table")
        self.artists = dbqueries.get_all_artists(connection=self.connection)
        self.artist_table = Table(
            frame=self.artist_display_frame,
            input_obj=self.artists
            )

        # Fill Artist search section
        self.artist_search_frame = ttk.LabelFrame(
            master=self.artist_frame,
            text="Search Artists"
            )
        self.artist_search_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.artist_search_frame.columnconfigure(index=0, weight=1)
        self.artist_search_frame.rowconfigure(
            index=0,
            weight=1,
            uniform="artist_search"
            )
        self.artist_search_frame.rowconfigure(
            index=1,
            weight=1,
            uniform="artist_search"
            )

        self.artist_search_textbox = TextBox(
            frame=self.artist_search_frame,
            row=0,
            column=0,
            sticky=tk.S
            )
        self.artist_search_button = ttk.Button(
            master=self.artist_search_frame,
            text="Search",
            command=lambda: self.search_artist())
        self.artist_search_button.grid(
            padx=2,
            pady=2,
            row=1,
            column=0,
            sticky=tk.N
            )

        def search_artist_return(event):
            self.search_artist()

        for self.widget in list(self.artist_search_frame.children.values()):
            self.widget.bind(sequence='<Return>', func=search_artist_return)

        # Fill Add Artist section
        self.artist_newitem_frame = ttk.LabelFrame(
            master=self.artist_frame,
            text="Add Artist"
            )
        self.artist_newitem_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.artist_newitem_frame.columnconfigure(index=0, weight=1)
        self.artist_newitem_frame.columnconfigure(index=1, weight=1)
        self.artist_newitem_frame.columnconfigure(index=2, weight=1)
        self.artist_newitem_frame.columnconfigure(index=3, weight=1)
        self.artist_newitem_frame.rowconfigure(
            index=0,
            weight=1,
            uniform="artist_add"
            )
        self.artist_newitem_frame.rowconfigure(
            index=1,
            weight=1,
            uniform="artist_add"
            )
        self.artist_newitem_frame.rowconfigure(
            index=2,
            weight=1,
            uniform="artist_add"
            )

        self.artist_name_label = ttk.Label(
            master=self.artist_newitem_frame,
            text="Name"
            )
        self.artist_name_label.grid(row=0, column=0, sticky=tk.SE)
        self.artist_name_textbox = TextBox(
            frame=self.artist_newitem_frame,
            row=0,
            column=1,
            sticky=tk.SW
            )

        self.artist_website_label = ttk.Label(
            master=self.artist_newitem_frame,
            text="Website"
            )
        self.artist_website_label.grid(row=0, column=2, sticky=tk.SE)
        self.artist_website_textbox = TextBox(
            frame=self.artist_newitem_frame,
            row=0,
            column=3,
            sticky=tk.SW
            )

        self.artist_email_label = ttk.Label(
            master=self.artist_newitem_frame,
            text="Email"
            )
        self.artist_email_label.grid(row=1, column=0, sticky=tk.NE)
        self.artist_email_textbox = TextBox(
            frame=self.artist_newitem_frame,
            row=1,
            column=1,
            sticky=tk.NW
            )

        self.artist_folder_label = ttk.Label(
            master=self.artist_newitem_frame,
            text="Folder"
            )
        self.artist_folder_label.grid(row=1, column=2, sticky=tk.NE)
        self.artist_folder_textbox = TextBox(
            frame=self.artist_newitem_frame,
            row=1,
            column=3,
            sticky=tk.NW
            )

        self.artist_submit_button = ttk.Button(
            master=self.artist_newitem_frame,
            text="Submit",
            command=lambda: self.add_artist()
            )
        self.artist_submit_button.grid(
            padx=2,
            pady=2,
            row=2,
            column=0,
            columnspan=4,
            sticky=tk.N
            )

        def add_artist_return(event):
            self.add_artist()

        for self.widget in list(self.artist_newitem_frame.children.values()):
            self.widget.bind(sequence='<Return>', func=add_artist_return)

        # Artist table commands
        self.artist_tablecommand_frame = ttk.LabelFrame(
            master=self.artist_frame,
            text="Table Commands"
            )
        self.artist_tablecommand_frame.grid(
            row=2,
            column=0,
            sticky=tk.NSEW,
            columnspan=2
            )
        self.artist_tablecommand_frame.columnconfigure(
            index=0,
            weight=1,
            uniform="artist_tablecommand"
            )
        self.artist_tablecommand_frame.columnconfigure(
            index=1,
            weight=1,
            uniform="artist_tablecommand"
            )

        self.artist_delete_button = ttk.Button(
            master=self.artist_tablecommand_frame,
            text="Delete",
            command=lambda: self.delete_artist()
            )

        self.artist_delete_button.grid(
            column=0,
            row=0,
            sticky=tk.NW,
            padx=5,
            pady=5
            )

        self.artist_export_button = ttk.Button(
            master=self.artist_tablecommand_frame,
            text="Export",
            command=lambda: self.export_table(table=self.artist_table)
            )

        self.artist_export_button.grid(
            column=1,
            row=0,
            sticky=tk.NW,
            padx=5,
            pady=5
            )

        self.tabs.add(child=self.artist_frame, text="Artists")

        # Create and populate Source tab
        self.source_frame = tk.Frame(master=self.tabs)
        self.source_frame.pack(padx=2, pady=2, fill=tk.BOTH, expand=tk.YES)
        self.source_frame.columnconfigure(index=0, weight=1)
        self.source_frame.columnconfigure(index=1, weight=5)
        self.source_frame.rowconfigure(index=0, weight=1, uniform="source")
        self.source_frame.rowconfigure(index=1, weight=5, uniform="source")
        self.source_frame.rowconfigure(index=2, weight=1)

        # Fill results table
        self.source_display_frame = ttk.LabelFrame(
            master=self.source_frame,
            text="Sources"
            )
        self.source_display_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.NSEW
            )

        logger.info("Populating source table")
        self.sources = dbqueries.get_all_sources(connection=self.connection)
        self.sources_table = Table(
            frame=self.source_display_frame,
            input_obj=self.sources
            )

        # Fill Source Search section
        self.source_search_frame = ttk.LabelFrame(
            master=self.source_frame,
            text="Search Sources"
            )
        self.source_search_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.source_search_frame.columnconfigure(index=0, weight=1)
        self.source_search_frame.rowconfigure(
            index=0,
            weight=1,
            uniform="source_search"
            )
        self.source_search_frame.rowconfigure(
            index=1,
            weight=1,
            uniform="source_search"
            )

        self.source_search_textbox = TextBox(
            frame=self.source_search_frame,
            row=0,
            column=0,
            sticky=tk.S
            )
        self.source_search_button = ttk.Button(
            master=self.source_search_frame,
            text="Search",
            command=lambda: self.search_source()
            )

        def search_source_return(event):
            self.search_source()

        for self.widget in list(self.source_search_frame.children.values()):
            self.widget.bind(sequence='<Return>', func=search_source_return)

        self.source_search_button.grid(
            padx=2,
            pady=2,
            row=1,
            column=0,
            sticky=tk.N
            )

        # Fill Add Source section
        self.source_newitem_frame = ttk.LabelFrame(
            master=self.source_frame,
            text="Add Source"
            )
        self.source_newitem_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.source_newitem_frame.columnconfigure(index=0, weight=1)
        self.source_newitem_frame.columnconfigure(index=1, weight=1)
        self.source_newitem_frame.columnconfigure(index=2, weight=1)
        self.source_newitem_frame.columnconfigure(index=3, weight=1)
        self.source_newitem_frame.rowconfigure(index=0,
            weight=1,
            uniform="source_add"
            )
        self.source_newitem_frame.rowconfigure(index=1,
            weight=1,
            uniform="source_add"
            )


        self.source_name_label = ttk.Label(
            master=self.source_newitem_frame,
            text="Name"
            )
        self.source_name_label.grid(row=0, column=0, sticky=tk.SE)
        self.source_name_textbox = TextBox(
            frame=self.source_newitem_frame,
            row=0,
            column=1,
            sticky=tk.SW
            )

        self.source_website_label = ttk.Label(
            master=self.source_newitem_frame,
            text="Website"
            )
        self.source_website_label.grid(row=0, column=2, sticky=tk.SE)
        self.source_website_textbox = TextBox(
            frame=self.source_newitem_frame,
            row=0,
            column=3,
            sticky=tk.SW
            )

        self.source_submit_button = ttk.Button(
            master=self.source_newitem_frame,
            text="Submit",
            command=lambda: self.add_source()
            )
        self.source_submit_button.grid(
            padx=2,
            pady=2,
            row=1,
            column=0,
            columnspan=4,
            sticky=tk.N
            )

        def add_source_return(event):
            self.add_source()

        for self.widget in list(self.source_newitem_frame.children.values()):
            self.widget.bind(sequence='<Return>', func=add_source_return)

        # Source table commands
        self.source_tablecommand_frame = ttk.LabelFrame(
            master=self.source_frame,
            text="Table Commands"
            )
        self.source_tablecommand_frame.grid(
            row=2,
            column=0,
            sticky=tk.NSEW,
            columnspan=2
            )
        self.source_tablecommand_frame.columnconfigure(
            index=0,
            weight=1,
            uniform="source_tablecommand"
            )
        self.source_tablecommand_frame.columnconfigure(
            index=1,
            weight=1,
            uniform="source_tablecommand"
            )

        self.source_tablecommand_delete_button = ttk.Button(
            master=self.source_tablecommand_frame,
            text="Delete",
            command=lambda: self.delete_source()
            )
        self.source_tablecommand_delete_button.grid(
            column=0,
            row=0,
            sticky=tk.NW,
            padx=5,
            pady=5
            )

        self.source_export_button = ttk.Button(
            master=self.source_tablecommand_frame,
            text="Export",
            command=lambda: self.export_table(self.sources_table)
            )
        self.source_export_button.grid(
            column=1,
            row=0,
            sticky=tk.NW,
            padx=5,
            pady=5
            )

        self.tabs.add(child=self.source_frame, text="Sources")

    def refresh_tables(self):
        """Replaces the tables and dropdowns with new data from the database.

        Pulls the latest data from the database and repopulates the three
        tables and the two model dropdowns.
        """
        logger.debug("Updating model list")
        self.updated_model_table = dbqueries.get_all_models(
            connection=self.connection
            )

        logger.debug("Updating artist list")
        self.updated_artist_table = dbqueries.get_all_artists(
            connection=self.connection
            )

        logger.debug("Updating source list")
        self.updated_source_table = dbqueries.get_all_sources(
            connection=self.connection
            )

        self.model_table.refresh_table(input_obj=self.updated_model_table)
        self.artist_table.refresh_table(input_obj=self.updated_artist_table)
        self.sources_table.refresh_table(input_obj=self.updated_source_table)

        logger.debug("Updating artist dropdown")
        self.refreshed_artists = dbqueries.get_all_artists(
            connection=self.connection
            )

        self.model_artist_dropdown.refresh_options(input=self.refreshed_artists)
        logger.debug("Updating source dropdown")
        self.refreshed_sources = dbqueries.get_all_sources(
            connection=self.connection
            )

        self.model_source_dropdown.refresh_options(input=self.refreshed_sources)

    def add_model(self):
        """Adds a new model to the database.

        Gathers the data that the user entered into the add model form
        and creates a model object to be inserted into the database. 
        After inserting the model, it refreshes the tables and
        dropdowns so that they reflect the new data.
        """
        self.new_model_entry = []
        # Adds a placeholder for the ID since it will be generated by
        # the database
        self.new_model_entry.append(0)
        self.new_model_entry.append(self.model_name_textbox.get_text())
        self.model_name_textbox.clear_text()
        self.new_model_entry.append(self.model_set_textbox.get_text())

        self._artist = self.model_artist_dropdown.get_selection()
        if self._artist:
            self.new_model_entry.append(self._artist)
        else:
            tkm.showwarning(
                title="Missing Artist",
                message="Please select an artist from the dropdown. If you "
                "need to enter a new artist, please do so from the Artist tab "
                "first."
                )
            return

        self._source = self.model_source_dropdown.get_selection()
        if self._source:
            self.new_model_entry.append(self._source)
        else:
            tkm.showwarning(
                title="Missing Source",
                message="Please select a source from the dropdown. If you "
                "need to enter a new source, please do so from the Source tab "
                "first."
                )
            return

        self.new_model_entry.append(self.model_source_note_textbox.get_text())
        self.new_model_entry.append(self.model_supports_chkbox.get_selection())
        self.new_model_entry.append(self.model_format_textbox.get_text())
        # Adds a placeholder because a folder is not needed
        self.new_model_entry.append('')
        self.new_model_entry.append(self.model_printed_chkbox.get_selection())

        self.new_model = self.factory.createModel(self.new_model_entry)

        logger.info("Adding model to the database")
        dbqueries.add_model(connection=self.connection, model=self.new_model)
        self.refresh_tables()

    def add_artist(self):
        """Adds a new artist to the database.

        Gathers the data that the user entered into the add artist form
        and creates an artist object to be inserted into the database. 
        After inserting the artist, it refreshes the tables and 
        dropdowns so that they reflect the new data.
        """
        self.new_artist_entry = []
        self.new_artist_entry.append(0)
        self.new_artist_entry.append(self.artist_name_textbox.get_text())
        self.artist_name_textbox.clear_text()
        self.new_artist_entry.append(self.artist_website_textbox.get_text())
        self.artist_website_textbox.clear_text()
        self.new_artist_entry.append(self.artist_email_textbox.get_text())
        self.artist_email_textbox.clear_text()
        self.new_artist_entry.append(self.artist_folder_textbox.get_text())
        self.artist_folder_textbox.clear_text()

        self.new_artist = self.factory.createArtist(self.new_artist_entry)
        logger.info("Adding artist to the database")
        dbqueries.add_artist(connection=self.connection, artist=self.new_artist)
        self.refresh_tables()

    def add_source(self):
        """Adds a new source to the database.

        Gathers the data that the user entered into the add source
        form and creates a source object to be inserted into the
        database. After inserting the source, it refreshes the tables
        and dropdown so that they reflect the new data.
        """
        self.new_source_entry = []
        self.new_source_entry.append(0)
        self.new_source_entry.append(self.source_name_textbox.get_text())
        self.source_name_textbox.clear_text()
        self.new_source_entry.append(self.source_website_textbox.get_text())
        self.source_website_textbox.clear_text()

        self.new_source = self.factory.createSource(self.new_source_entry)
        logger.info("Adding source to the database")
        dbqueries.add_source(connection=self.connection, source=self.new_source)
        self.refresh_tables()

    def search_models(self):
        """Searches the database for models matching a search term.

        Gathers the user's search term and selected field to search
        and returns the matching rows as a model object then refreshes
        the model table so that it will reflect the newly entered data.

        Returns:
            A list of model objects matching the query
        """
        self.model_search_term = self.model_search_textbox.get_text()
        self.model_search_textbox.clear_text()
        self.model_search_field = self.model_search_selected.get()

        if self.model_search_field:
            logger.info("Searching models")
            logger.debug(
                f"{self.model_search_term} in {self.model_search_field}"
                )
            if self.model_search_field == "Artist":
                self.search_artist_id = dbqueries.get_artist_id(
                    connection=self.connection,
                    artist_name=self.model_search_term
                    )
                self.model_results = dbqueries.search_associated_models(
                    connection=self.connection,
                    field="Artist",
                    search_id=self.search_artist_id
                    )
                try:
                    self.model_table.refresh_table(input_obj=self.model_results)
                except TypeError:
                    logger.warning("No Models Found")
            elif self.model_search_field == "Source":
                self.search_source_id = dbqueries.get_source_id(
                    connection=self.connection,
                    source_name=self.model_search_term
                    )
                self.model_results = dbqueries.search_associated_models(
                    connection=self.connection,
                    field="Source",
                    search_id=self.search_source_id
                    )
                try:
                    self.model_table.refresh_table(input_obj=self.model_results)
                except TypeError:
                    logger.warning("No Models Found")
            else:
                self.model_results = dbqueries.search_model(
                    connection=self.connection,
                    field=self.model_search_field,
                    search_text=self.model_search_term
                    )
                try:
                    self.model_table.refresh_table(input_obj=self.model_results)
                except TypeError:
                    logger.warning("No Models Found")
        else:
            logger.warning("Missing search field")
            tkm.showwarning(
                title="Missing Field",
                message="The search field is missing. "
                    "Please select a search field from the dropdown box and "
                    "try again."
                )

    def search_artist(self):
        """Searches the database for artists matching a search term.

        Gathers the user's search term and returns the matching rows
        as an artist object then refreshes the artist table so that 
        it will reflect the newly entered data.

        Returns:
            A list of artist objects matching the query
        """
        self.artist_search_term = self.artist_search_textbox.get_text()
        self.artist_search_textbox.clear_text()

        logger.info("Searching artists")
        self.artist_results = dbqueries.search_artist(
            connection=self.connection,
            search_text=self.artist_search_term
            )
        try:
            self.artist_table.refresh_table(input_obj=self.artist_results)
        except TypeError:
            logger.warning("No Artists Found")

    def search_source(self):
        """Searches the database for sources matching a search term.

        Gathers the user's search term and returns the matching rows
        as a source object then refreshes the sources table so that 
        it will reflect the newly entered data.

        Returns:
            A list of source objects matching the query
        """
        self.source_search_term = self.source_search_textbox.get_text()
        self.source_search_textbox.clear_text()

        logger.info("Searching sources")
        self.search_results = dbqueries.search_source(
            connection=self.connection,
            search_text=self.source_search_term
            )
        try:
            self.sources_table.refresh_table(input_obj=self.search_results)
        except TypeError:
            logger.warning("No Sources Found")

    def delete_model(self) -> None:
        """Deletes a model from the database."""
        self.selected = self.model_table.get_selected_rows()
        self.delete_choice = tkm.askyesno(
            title="Delete Model", 
            message=f"Do you want to delete {len(self.selected)} model(s)?"
            )
        if self.delete_choice:
            for self.selected_model in self.selected:
                logger.info(f"Deleting Model_ID: {self.selected_model[0]}")
                dbqueries.delete_model(
                    connection=self.connection,
                    model_id=self.selected_model[0]
                    )
            self.refresh_tables()

    def delete_artist(self) -> None:
        """Deletes an artist from the database."""
        self.selected = self.artist_table.get_selected_rows()
        self.delete_choice = tkm.askyesno(
            title="Delete Artist",
            message=f"Do you want to delete {len(self.selected)} artist(s)?"
            )
        if self.delete_choice:
            for self.selected_artist in self.selected:
                self.associated_models = dbqueries.search_associated_models(
                    connection=self.connection,
                    field='Artist',
                    search_id=self.selected_artist[0]
                    )
                if not len(self.associated_models):  # type: ignore
                    logger.info(f"Deleting Artist_ID: {self.selected_artist[0]}")
                    dbqueries.delete_artist(
                        connection=self.connection,
                        artist_id=self.selected_artist[0]
                        )
                else:
                    self.associated_model_warning = tkm.showwarning(
                        title="Associated Models", 
                        message="This artist is associated with models. "
                            "Please delete the associated models before "
                            "deleting the artist."
                    )
                    logger.warning(
                        f"Artist {self.selected_artist[0]} has associated models"
                        )
            self.refresh_tables()

    def delete_source(self) -> None:
        """Deletes a source from the database."""
        self.selected = self.sources_table.get_selected_rows()
        self.delete_choice = tkm.askyesno(
            title="Delete Source",
            message=f"Do you want to delete {len(self.selected)} source(s)?"
            )
        if self.delete_choice:
            for self.selected_source in self.selected:
                self.associated_models = dbqueries.search_associated_models(
                    connection=self.connection,
                    field='Source',
                    search_id=self.selected_source[0]
                    )
                if not len(self.associated_models):  # type: ignore
                    logger.info(f"Deleting Source_ID: {self.selected_source[0]}")
                    dbqueries.delete_source(
                        connection=self.connection,
                        source_id=self.selected_source[0]
                        )
                else:
                    self.associated_model_warning = tkm.showwarning(
                        title="Associated Models", 
                        message="This source is associated with models. "
                            "Please delete the associated models before "
                            "deleting the source."
                    )
                    logger.warning(
                        f"Source {self.selected_source[0]} has associated models"
                        )
            self.refresh_tables()

    def export_table(self, table) -> None:
        self.selected_table = table
        self.exported_rows = self.selected_table.get_all_rows()
        self.default_export = pathlib.Path.home().joinpath('export.csv')
        self.export_location = tkf.asksaveasfilename(
            title="Save File",
            initialdir=self.default_export,
            initialfile='export.csv',
            filetypes=(("Comma Separated Values", "*.csv"),)
            )
        if self.export_location:
            self.export_file = pathlib.Path(self.export_location)
            with open(file=self.export_file, mode='w', newline='') as self.export:
                self.export_writer = csv.writer(
                    self.export,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL
                    )
                self.export_writer.writerow(self.selected_table.columns)
                for self.exported_row in self.exported_rows:
                    self.export_writer.writerow(self.exported_row)


def focus_next_widget(event):
    """Focuses the next widget in focus order"""
    event.widget.tk_focusNext().focus()
    # Break is here to prevent the rebound key from performing its original
    # function
    return("break")


class Table:
    """Creates a table from the passed objects in the specified frame.

    This class takes a list of one or more input objects and uses that
    data to create a table in the specified frame. The object's 
    attribute names become the header names and each object is added 
    as a row to the new table. Methods are also provided to clear the
    table and to refresh the table with new data.
    """
    def __init__(self, frame, input_obj):
        """Creates an empty table.

        Creates an empty table in the specified frame using data from
        an input object. 

        Args:
            frame: The frame that the table should be created in.
            input_obj: The object used to populate the table.
        """
        self.frame = frame
        self.input_obj = input_obj
        self.scroll = ttk.Scrollbar(master=self.frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.table = ttk.Treeview(master=frame, yscrollcommand=self.scroll.set)
        self.table.pack(padx=2, pady=2, expand=True, fill=tk.BOTH)
        self.scroll.config(command=self.table.yview)

        try:
            self.add_rows(input_obj=self.input_obj)
        except TypeError:
            logger.warning("No entries found")

    def add_rows(self, input_obj):
        """Adds rows to the table from a supplied object.

        Takes an list of objects and uses its attributes to create the
        headers and enters one object per row in the table.

        Args:
            input_obj: A list of model, artist, or source objects.
        """
        self.input_obj = input_obj
        # Checking to see if self.input_obj is a list or an individual object
        # before proceeding.
        try:
            self.column_names_temp = vars(self.input_obj[0])
        except (IndexError, TypeError):
            self.column_names_temp = vars(self.input_obj)

        self.column_names = self.column_names_temp.keys()

        self.columns = []
        for self.name in self.column_names:
            self.columns.append(self.name)

        self.table['columns'] = self.columns

        self.table.column(column='#0', width=0, stretch=tk.NO)
        self.table.heading(column='#0', text="", anchor=tk.W)
        for self.heading in self.column_names:
            self.table.column(column=self.heading, anchor=tk.W, width=80)
            self.table.heading(
                column=self.heading,
                text=self.heading.capitalize(),
                anchor=tk.W,
                command=lambda col=self.heading: self.sort_table(col, False)
                )

        # Checking to see if self.input_obj is a list or an individual object
        # before proceeding.
        try:
            for self.row in self.input_obj:
                self.table.insert(
                    parent='',
                    index=tk.END,
                    values=(self.row.astuple())
                    )
        except TypeError:
            self.table.insert(
                parent='',
                index=tk.END,
                values=(self.input_obj.astuple())
                )

    def clear_table(self):
        """Clears the data from the table."""
        for item in self.table.get_children():
            self.table.delete(item)

    def refresh_table(self, input_obj):
        """Replaces the data in the table.

        Takes the data from the input object and repopulates the table
        with that data.

        Args:
            input_obj: A list of model, artist, or source objects.
        """
        self.input_obj = input_obj
        self.clear_table()
        try:
            self.add_rows(input_obj=self.input_obj)
        except TypeError:
            logger.warning("No rows to update")

    def sort_table(self, column: str, descending: bool) -> None:
        """Sorts the table by the selected column.

        Args:
            column: The column to sort by
            descending: Whether to sort descending or not
        """
        data = []
        for child in self.table.get_children(''):
            temp = [self.table.set(item=child, column=column), child]
            temp[0] = temp[0].lower()
            data.append(temp)

        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.table.move(item[1], '', indx)

        self.table.heading(
            column=column,
            command=lambda col=column: self.sort_table(col, bool(not descending))
            )

    def get_selected_rows(self) -> tuple:
        """Returns the selected row."""
        self.selected = (
            self.table.item(self.selected)['values'] 
            for self.selected in self.table.selection()
            )
        return tuple(self.selected)

    def get_all_rows(self) -> tuple:
        self.rows = (
            self.table.item(self.child)['values']
            for self.child in self.table.get_children()
            )
        return tuple(self.rows)

class TextBox:
    """ Creates a text entry box.

    Creates a text entry box in the specified frame with the specified
    grid options.
    """
    def __init__(self, frame, row, column, sticky):
        """Inits the new text entry box.

        Args:
            frame: The frame that the text box will be created in.
            row: Grid row the widget is in.
            column: Grid column the widget is in.
            sticky: where in the column/row the widget is attached.
        """
        self.frame = frame
        self.row = row
        self.column = column
        self.sticky = sticky

        self.text_box = ttk.Entry(master=self.frame, width=30)
        self.text_box.grid(
            padx=2,
            pady=2,
            row=self.row,
            column=self.column,
            sticky=self.sticky
            )
        self.text_box.bind(sequence='<Tab>', func=focus_next_widget)

    def get_text(self):
        """Retrieves the text from the text box.

        Returns:
            A string containing the text entered in the text box.
        """
        self.input = self.text_box.get()
        return self.input

    def clear_text(self):
        """Removes the text from the text box."""
        self.text_box.delete(0, tk.END)


class DropdownBox:
    """ Creates a dropdown box.

    Creates a dropdown box in the specified frame with the specified
    grid options.
    """
    def __init__(self, frame, input_obj, row, column, sticky):
        """Inits the new text entry box.

        Sets the text box's size, side, and anchor position.

        Args:
            frame: The frame that the text box will be created in.
            input_obj: The object used to populate the options.
            row: Grid row the widget is in.
            column: Grid column the widget is in.
            sticky: where in the column/row the widget is attached.
        """
        self.frame = frame
        self.row = row
        self.column = column
        self.sticky = sticky
        self.input_obj = input_obj
        self.var = tk.StringVar()
        self.options = []

        if self.input_obj:
            try:
                for self.item in self.input_obj:
                    self.options.append(self.item.name)
            except (IndexError, TypeError):
                self.options.append(self.input_obj.name)
            self.options.sort(key=str.lower)
        else:
            self.options.append("Empty")

        self.dropdown = ttk.OptionMenu(
            self.frame,
            self.var,
            "Please Select",
            *self.options
            )
        self.dropdown.grid(
            padx=2,
            pady=2,
            row=self.row,
            column=self.column,
            sticky=self.sticky
            )

    def get_selection(self):
        """Gets the selected item.

        Retrieves the selected item from the dropdown box.

        Returns:
            A string containing the user's selection.
        """
        self.value = self.var.get()
        if self.value == "Please Select":
            return None
        else:
            return self.var.get()

    def refresh_options(self, input):
        """Replaces the data in the dropdown.

        Takes the data from the input object and repopulates the
        dropdown with that data.

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

    Creates a dropdown box in the specified frame with the specified
    grid options.
    """
    def __init__(self, frame, text, row, column, sticky):
        """Inits the new  checkbox.

        Sets the checkbox's size, side, and anchor position.

        Args:
            frame: The frame that the text box will be created in.
            text: The text for the builtin label.
            row: Grid row the widget is in
            column: Grid column the widget is in
            sticky: where in the column/row the widget is attached
        """
        self.frame = frame
        self.row = row
        self.column = column
        self.sticky = sticky
        self.text = text
        self.var = tk.BooleanVar()

        self.checkbox = ttk.Checkbutton(
            self.frame, 
            text=self.text,
            onvalue=tk.TRUE,
            offvalue=tk.FALSE,
            variable=self.var
            )
        self.checkbox.grid(
            padx=2,
            pady=2,
            row=self.row,
            column=self.column,
            sticky=self.sticky
            )

    def get_selection(self):
        """Gets the selected item.

        Retrieves the state of the checkbox.

        Returns:
            A boolean with the selected state of the checkbox.
        """
        return self.var.get()

    def clear_selection(self):
        """Reset the checkbox to the initial state of False"""
        self.checkbox.state(['!selected'])
