import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject
from app.utils.color import Color
from app.ui.widgets.sv_selector import SVSelector
from app.ui.widgets.hue_slider import HueSlider
from app.ui.widgets.color_view import ColorView, ColorViewType
import colorsys, cairo


class HSVPickerWindow(Gtk.Window):

    __gsignals__ = {
        "color_selected": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    def __init__(self, app: Gtk.Application, color: Color):
        super().__init__(title="HSV Picker")

        self.set_default_size(360, 280)
        self.color = color.copy()

        self.build_ui()


    def build_ui(self) -> None:
        root_child = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        root_child.add_css_class("window-root-child")
        self.set_child(root_child)
        
        first_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        root_child.append(first_row)
        second_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        root_child.append(second_row)

        hue, saturation, value = self.color.hsv

        # 2D HSV area
        self.hs_selector = SVSelector(hue=hue, saturation=saturation, value=value)
        self.hs_selector.connect("sv-changed", self.on_sv_changed)
        first_row.append(self.hs_selector)

        # hue slider
        self.hue_slider = HueSlider(initial_hue=hue)
        self.hue_slider.connect("hue_changed", self.on_hue_changed)
        first_row.append(self.hue_slider)

        # color preview
        self.color_preview = ColorView(120, 30, self.color, ColorViewType.SQUARE, False)
        second_row.append(self.color_preview)

        # buttons
        buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        buttons.set_halign(Gtk.Align.CENTER)
        cancel = Gtk.Button(label="Cancel")
        cancel.connect("clicked", lambda *_: self.close())
        ok = Gtk.Button(label="Apply")
        ok.add_css_class("suggested-action")
        ok.connect("clicked", self.on_apply_color)
        buttons.append(cancel)
        buttons.append(ok)
        second_row.append(buttons)


    # actions when we select values from the sv area
    def on_sv_changed(self, widget, s, v)->None:
        hue, saturation, value = self.color.hsv
        self.color.hsv = hue, s, v
        self.color_preview.set_color(self.color)


    # actions to take when we the hue value is changed from the slider
    def on_hue_changed(self, widget, h):
        hue, saturation, value = self.color.hsv
        self.color.hsv = h, saturation, value
        self.hs_selector.set_hue(hue)
        self.color_preview.set_color(self.color)


    # select color and close the window
    def on_apply_color(self, *_)->None:
        self.emit("color_selected", self.color)
        self.close()


    



