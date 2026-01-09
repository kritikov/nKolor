from gi.repository import Gtk, GObject
from app.ui.widgets.color_value_bar import ColorValueBar
from app.utils.color import Color

class ColorValues(Gtk.Box):
    
    __gsignals__ = {
        "edit_rgb": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit_hsl": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit_hsv": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.set_hexpand(True)
        self.hex_bar = ColorValueBar("HEX", "")
        self.rgb_bar = ColorValueBar("RGB", "")
        self.rgb_bar.connect("edit", lambda w: self.emit("edit_rgb"))

        self.hsl_bar = ColorValueBar("HSL", "")
        self.hsl_bar.connect("edit", lambda w: self.emit("edit_hsl"))

        self.hsv_bar = ColorValueBar("HSV", "")
        self.hsl_bar.connect("edit", lambda w: self.emit("edit_hsv"))

        self.append(self.hex_bar)
        self.append(self.rgb_bar)
        self.append(self.hsl_bar)
        self.append(self.hsv_bar)

    def set_color(self, color: Color):
        self.hex_bar.set_value(color.hex)
        self.rgb_bar.set_value(color.rgb)
        self.hsl_bar.set_value(color.hsl)
        self.hsv_bar.set_value(color.hsv)