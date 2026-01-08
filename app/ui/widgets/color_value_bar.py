from gi.repository import Gtk, Gdk, GObject

class ColorValueBar(Gtk.Box):
    
    __gsignals__ = {
        "copy": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self, title: str, value: str):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        self.add_css_class("value-bar")
        self.build_ui(title, value)
        

    def build_ui(self, title: str, value: str):
        title_lbl = Gtk.Label(label=f"{title}:")
        title_lbl.set_size_request(50, -1)
        title_lbl.set_xalign(0)
        self.append(title_lbl)

        values_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.append(values_container)

        self.value_entry = Gtk.Entry()
        self.value_entry.set_editable(False)        
        self.value_entry.set_can_focus(True)        
        self.value_entry.set_hexpand(True)
        self.value_entry.set_text(value)
        self.value_entry.add_css_class("value-text")
        values_container.append(self.value_entry)

        self.copy_btn = Gtk.Button()
        copy_icon = Gtk.Image.new_from_file("app/resources/icons/copy.png")
        copy_icon.set_pixel_size(30)
        self.copy_btn.set_child(copy_icon);
        self.copy_btn.set_tooltip_text("copy to clipboard")
        self.copy_btn.connect("clicked", self.copy_to_clipboard)
        values_container.append(self.copy_btn)


        self.edit_btn = Gtk.Button()
        edit_icon = Gtk.Image.new_from_file("app/resources/icons/edit.png")
        edit_icon.set_pixel_size(30)
        self.edit_btn.set_child(edit_icon);
        self.edit_btn.set_tooltip_text("edit the color")
        self.edit_btn.connect("clicked", lambda w: self.emit("edit"))
        values_container.append(self.edit_btn)


    # copy the value in the clipboard
    def copy_to_clipboard(self, *_):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(self.value_entry.get_text())
        self.emit("copy")


    # set the value
    def set_value(self, value: str):
        text = self.value_entry.set_text(value)
