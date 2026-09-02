from gi.repository import Gtk, Gdk, GObject
from nkolor.resources.resources import Resources

class ColorValueBar(Gtk.Box):
    
    __gsignals__ = {
        "copy": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self, title: str, value: str, button_size: int = 28):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        self.add_css_class("value-bar")
        self.build_ui(title, value, button_size)
        

    def build_ui(self, title: str, value: str, button_size: int)-> None:
        title_lbl = Gtk.Label(label=f"{title}:")
        title_lbl.set_xalign(0)
        self.append(title_lbl)

        values_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.append(values_container)

        self.value_entry = Gtk.Entry()
        self.value_entry.set_editable(False)        
        self.value_entry.set_can_focus(True)        
        self.value_entry.set_hexpand(True)
        self.value_entry.set_text(value)
        values_container.append(self.value_entry)

        self.copy_btn = Gtk.Button()
        self.copy_btn.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.copy_btn.add_css_class("color-values-button")
        copy_icon = Gtk.Image.new_from_file(Resources.icon("copy.png"))
        copy_icon.set_pixel_size(button_size)
        self.copy_btn.set_child(copy_icon);
        self.copy_btn.set_tooltip_text("copy to clipboard")
        self.copy_btn.connect("clicked", self.copy_to_clipboard)
        values_container.append(self.copy_btn)


        self.edit_btn = Gtk.Button()
        self.edit_btn.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        self.edit_btn.add_css_class("color-values-button")
        edit_icon = Gtk.Image.new_from_file(Resources.icon("edit.png"))
        edit_icon.set_pixel_size(button_size)
        self.edit_btn.set_child(edit_icon);
        self.edit_btn.set_tooltip_text("edit the color")
        self.edit_btn.connect("clicked", lambda w: self.emit("edit"))
        values_container.append(self.edit_btn)


    # copy the value in the clipboard
    def copy_to_clipboard(self, *_)-> None:
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(self.value_entry.get_text())
        self.emit("copy")


    # set the value
    def set_value(self, value: str)-> None:
        text = self.value_entry.set_text(value)
