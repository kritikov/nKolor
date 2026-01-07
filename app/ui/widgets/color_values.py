from gi.repository import Gtk
from app.ui.widgets.color_value_bar import ColorValueBar
from app.utils.color import Color

class ColorValues(Gtk.Box):
    
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.set_hexpand(True)
        self.hex_bar = ColorValueBar("HEX", "")
        self.rgb_bar = ColorValueBar("RGB", "")
        self.hsl_bar = ColorValueBar("HSL", "")
        self.hsv_bar = ColorValueBar("HSV", "")

        self.append(self.hex_bar)
        self.append(self.rgb_bar)
        self.append(self.hsl_bar)
        self.append(self.hsv_bar)

    def set_color(self, color: Color):
        self.hex_bar.set_value(color.hex)
        self.rgb_bar.set_value(color.rgb)
        self.hsl_bar.set_value(color.hsl)
        self.hsv_bar.set_value(color.hsv)