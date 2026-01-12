from gi.repository import Gtk, Gdk, GObject
from app.utils.color import Color
from app.ui.widgets.color_view import ColorView, ColorViewType
from app.ui.widgets.slider_editor import SliderEditor
from app.ui.widgets.slider_editor import SliderEditorFormat


class HsvEditorWindow(Gtk.ApplicationWindow):

    __gsignals__ = {
            "color_selected": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
        }

    def __init__(self, app: Gtk.Application, color: Color):
        super().__init__(application=app, title="HSV editor")

        self.set_default_size(370, -1)
        self.set_resizable(False) 
        self.color = color.copy()
        self.build_ui()

        # Key controller για ESC
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

    def build_ui(self)->None:
        root_child = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        root_child.add_css_class("window-root-child")
        self.set_child(root_child)

        hue, saturation, value = self.color.hsv_for_ui

        # inputs
        hue_editor = SliderEditor("Hue", hue, 0, 360, SliderEditorFormat.INTEGER, 90)
        hue_editor.connect("value_changed", self.on_hue_changed)
        root_child.append(hue_editor)

        saturation_editor = SliderEditor("Saturation", saturation, 0, 100, SliderEditorFormat.INTEGER, 90)
        saturation_editor.connect("value_changed", self.on_saturation_changed)
        root_child.append(saturation_editor)

        value_editor = SliderEditor("Value", value, 0, 100, SliderEditorFormat.INTEGER, 90)
        value_editor.connect("value_changed", self.on_value_changed)
        root_child.append(value_editor)

        # bottom row
        bottom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        root_child.append(bottom_row)

        # color preview
        self.color_preview = ColorView(120, 30, self.color, ColorViewType.SQUARE, False)
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


    def on_hue_changed(self, widget, new_value:int)->None:
        hue, saturation, value = self.color.hsv_for_ui
        hue = new_value
        self.color.hsv_for_ui = hue, saturation, value
        self.update_preview()

    def on_saturation_changed(self, widget, new_value:int)->None:
        hue, saturation, value = self.color.hsv_for_ui
        saturation = new_value
        self.color.hsv_for_ui = hue, saturation, value
        self.update_preview()

    def on_value_changed(self, widget, new_value:int)->None:
        hue, saturation, value = self.color.hsv_for_ui
        value = new_value
        self.color.hsv_for_ui = hue, saturation, value
        self.update_preview()

    def update_preview(self)->None:
        self.color_preview.set_color(self.color)

    def on_apply_color(self, *_)->None:
        self.emit("color_selected", self.color)
        self.close()


    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.close()
            return True
        elif keyval == Gdk.KEY_Return or keyval == Gdk.KEY_KP_Enter:
            self.emit("color_selected", self.color)
            self.close()
            return True
        return False
    
