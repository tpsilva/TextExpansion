from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Text Expansion")

        self.set_border_width(10)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)

        # File selection
        self.top_hbox = Gtk.Box(spacing=6)
        self.vbox.pack_start(self.top_hbox, True, True, 0)

        self.label = Gtk.Label("File: ")
        self.top_hbox.pack_start(self.label, True, True, 0)

        self.file_entry = Gtk.Entry()
        self.top_hbox.pack_start(self.file_entry, True, True, 0)

        self.select_button = Gtk.Button(label="Select...")
        self.select_button.connect("clicked", self.select_button_clicked)
        self.top_hbox.pack_start(self.select_button, True, True, 0)

        # Expansion parameters
        self.parameters_hbox = Gtk.Box(spacing=6)
        self.vbox.pack_start(self.parameters_hbox, True, True, 0)

        self.lingo_toggle = Gtk.ToggleButton("Lingo")
        self.parameters_hbox.pack_start(self.lingo_toggle, True, True, 0)

        self.original_toggle = Gtk.ToggleButton("Original")
        self.parameters_hbox.pack_start(self.original_toggle, True, True, 0)

        self.concepts_toggle = Gtk.ToggleButton("Concepts")
        self.parameters_hbox.pack_start(self.concepts_toggle, True, True, 0)

        self.disambiguation_toggle = Gtk.ToggleButton("Disambiguation")
        self.parameters_hbox.pack_start(self.disambiguation_toggle, True, True, 0)

        # Custom dictionaries
        self.custom_dict_liststore = Gtk.ListStore(str)
        self.custom_dict_treeview = Gtk.TreeView(model=self.custom_dict_liststore)
        self.custom_dict_treeview.set_size_request(200, 200)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Custom Dictionaries", renderer_text, text=0)
        self.custom_dict_treeview.append_column(column_text)

        self.vbox.pack_start(self.custom_dict_treeview, True, True, 0)

        # Add and remove buttons
        self.buttons_hbox = Gtk.Box(spacing=6)
        self.vbox.pack_start(self.buttons_hbox, True, True, 0)

        self.add_button = Gtk.Button("Add")
        self.add_button.connect("clicked", self.add_button_clicked)
        self.buttons_hbox.pack_start(self.add_button, True, True, 0)

        self.remove_button = Gtk.Button("Remove")
        self.remove_button.connect("clicked", self.remove_button_clicked)
        self.buttons_hbox.pack_start(self.remove_button, True, True, 0)

        # Expand button
        self.expand_button = Gtk.Button("Expand")
        self.expand_button.connect("clicked", self.expand_button_clicked)
        self.vbox.pack_start(self.expand_button, True, True, 0)

    def select_button_clicked(self, widget):
        select_dialog = Gtk.FileChooserDialog("Choose file to expand", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = select_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_entry.set_text(select_dialog.get_filename())

        select_dialog.destroy()

    def add_button_clicked(self, widget):
        select_dialog = Gtk.FileChooserDialog("Choose a custom dictionary", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = select_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.custom_dict_liststore.append([select_dialog.get_filename()])

        select_dialog.destroy()

    def remove_button_clicked(self, widget):
        selection = self.custom_dict_treeview.get_selection()
        result = selection.get_selected()

        if result is not None and None not in result:
            model, iter = result
            model.remove(iter)
    
    def expand_button_clicked(self, widget):
        print "TODO"

    def run(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

        Gtk.main()

