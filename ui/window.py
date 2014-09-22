from gi.repository import Gtk, GObject
import thread

from expansion import expansion

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Text Expansion")

        self.set_resizable(False)
        self.set_border_width(10)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)

        # Menu
        self.menu = Gtk.MenuBar()
        self.vbox.pack_start(self.menu, True, True, 0)

        self.settings_item = Gtk.MenuItem("Settings")
        self.menu.append(self.settings_item)

        self.settings_submenu = Gtk.Menu()
        self.settings_item.set_submenu(self.settings_submenu)

        self.use_wordnet = Gtk.CheckMenuItem("Use wordnet")
        self.settings_submenu.append(self.use_wordnet)
        self.use_wordnet.set_active(True)

        self.use_wikipedia = Gtk.CheckMenuItem("Use wikipedia")
        self.settings_submenu.append(self.use_wikipedia)
        self.use_wikipedia.set_active(True)

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
        self.concepts_toggle.connect("toggled", self.concepts_toggle_toggled)
        self.parameters_hbox.pack_start(self.concepts_toggle, True, True, 0)

        self.disambiguation_toggle = Gtk.ToggleButton("Disambiguation")
        self.disambiguation_toggle.connect("toggled", self.disambiguation_toggle_toggled)
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

    def concepts_toggle_toggled(self, widget):
        if widget.get_active():
            self.disambiguation_toggle.set_active(not widget.get_active())

    def disambiguation_toggle_toggled(self, widget):
        if widget.get_active():
            self.concepts_toggle.set_active(not widget.get_active())

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
        self.progress = ProgressWindow()
        self.progress.start()

        thread.start_new_thread(self.expand_sample, ())

    def expand_sample(self):
        input_file = open(self.file_entry.get_text())
        samples = [l.strip("\n") for l in input_file.readlines()]
        input_file.close()

        custom_dictionaries = map(lambda x: x[0], self.custom_dict_liststore)

        expanded_samples = expansion.expand(samples,
            (self.lingo_toggle.get_active(), self.original_toggle.get_active(), 
            self.concepts_toggle.get_active(), self.disambiguation_toggle.get_active()),
            (self.use_wordnet.get_active(), self.use_wikipedia.get_active()),
            *custom_dictionaries)

        output_file = open(self.file_entry.get_text() + "_expanded.txt", "w")
        output_file.write("\n".join(expanded_samples))
        output_file.close()

        self.progress.stop()

    def run(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

        Gtk.main()


class ProgressWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Please wait")

        self.set_resizable(False)
        self.set_border_width(10)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)

        self.label = Gtk.Label("Expanding...")
        self.vbox.pack_start(self.label, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        self.vbox.pack_start(self.progressbar, True, True, 0)

    def start(self):
        self.show_all()
        self.set_modal(True)
        self.should_continue = True
        
        GObject.timeout_add(50, self.show_progress)

    def stop(self):
        self.should_continue = False
        self.destroy()

    def show_progress(self):
        self.progressbar.pulse()
        return self.should_continue

