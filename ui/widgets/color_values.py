from gi.repository import Gtk, GObject
from nkolor.ui.widgets.color_value_bar import ColorValueBar
from nkolor.utils.color import Color

class ColorValues(Gtk.Box):
    
    __gsignals__ = {
        "edit_hex": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit_rgb": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit_hsl": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit_hsv": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    def __init__(self, button_size: int = 28):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.set_hexpand(True)
        self.hex_bar = ColorValueBar("HEX", "", button_size)
        self.hex_bar.connect("edit", lambda w: self.emit("edit_hex"))

        self.rgb_bar = ColorValueBar("RGB", "", button_size)
        self.rgb_bar.connect("edit", lambda w: self.emit("edit_rgb"))

        self.hsl_bar = ColorValueBar("HSL", "", button_size)
        self.hsl_bar.connect("edit", lambda w: self.emit("edit_hsl"))

        self.hsv_bar = ColorValueBar("HSV", "", button_size)
        self.hsv_bar.connect("edit", lambda w: self.emit("edit_hsv"))

        self.append(self.hex_bar)
        self.append(self.rgb_bar)
        self.append(self.hsl_bar)
        self.append(self.hsv_bar)

    def set_color(self, color: Color)-> None:
        self.hex_bar.set_value(color.hex_text)
        self.rgb_bar.set_value(color.rgb_text)
        self.hsl_bar.set_value(color.hsl_text)
        self.hsv_bar.set_value(color.hsv_text)