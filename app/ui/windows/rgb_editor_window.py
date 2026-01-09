from gi.repository import Gtk, GObject
from app.utils.color import Color
from app.ui.widgets.color_view import ColorView
from app.ui.widgets.color_view import ColorViewType
from app.ui.widgets.slider_editor import SliderEditor


class RgbEditorWindow(Gtk.ApplicationWindow):

    __gsignals__ = {
            "color_selected": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
        }

    def __init__(self, app: Gtk.Application, color: Color):
        super().__init__(application=app, title="RGB editor")

        # self.set_default_size(500, 220)
        self.set_resizable(False) 
        self.color = color.copy()
        self.build_ui()

    def build_ui(self):
        root_child = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        root_child.add_css_class("window-root-child")
        self.set_child(root_child)

        red, green, blue = self.color.rgb

        # inputs
        red_editor = SliderEditor("R", red, 0, 255)
        red_editor.connect("value_changed", self.on_red_changed)
        root_child.append(red_editor)

        green_editor = SliderEditor("G", green, 0, 255)
        green_editor.connect("value_changed", self.on_green_changed)
        root_child.append(green_editor)

        blue_editor = SliderEditor("B", blue, 0, 255)
        blue_editor.connect("value_changed", self.on_blue_changed)
        root_child.append(blue_editor)

        # bottom row
        bottom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        root_child.append(bottom_row)

        # color preview
        self.color_preview = ColorView(120, 30, self.color, ColorViewType.SQUARE)
        bottom_row.append(self.color_preview)

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
        bottom_row.append(buttons)


    def on_red_changed(self, widget, value):
        red, green, blue = self.color.rgb
        red = value
        self.color.rgb = red, green, blue
        self.update_preview()

    def on_green_changed(self, widget, value):
        red, green, blue = self.color.rgb
        green = value
        self.color.rgb = red, green, blue
        self.update_preview()

    def on_blue_changed(self, widget, value):
        red, green, blue = self.color.rgb
        blue = value
        self.color.rgb = red, green, blue
        self.update_preview()

    def update_preview(self):
        self.color_preview.set_color(self.color)

    def on_apply_color(self, *_):
        self.emit("color_selected", self.color)
        self.close()


    
