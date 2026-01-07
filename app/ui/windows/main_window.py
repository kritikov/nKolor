import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk
from app.ui.widgets.history_bar import HistoryBar
from app.ui.widgets.pick_button import PickButton
from app.ui.widgets.color_preview import ColorPreview
from app.ui.widgets.color_values import ColorValues
from app.utils.color import Color
from app.ui.windows.magnifier_window import MagnifierWindow

class MainWindow(Gtk.ApplicationWindow) : 

    def __init__(self, app: Gtk.ApplicationWindow) -> None:
        super().__init__(application=app)
        self.set_title("nKolor")
        self.set_default_size(500, 220)
        self.set_resizable(False) 
        self.picking = False

        self.magnifier = MagnifierWindow()
        self.active = False

        self.build_ui()


    def build_ui(self) -> None:
        root_child = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=12)
        root_child.add_css_class("main-window")

        # general cunstruction
        left_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        right_col = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=12)
        root_child.append(left_col)
        root_child.append(right_col)
        self.set_child(root_child)  

        # elements
        self.pick_button = PickButton()
        self.pick_button.connect("pressed", self.on_start_pick_mode)
        self.pick_button.connect("released", self.on_stop_pick_mode)
        self.pick_button.connect("aborted", self.on_magnifier_aborted)
        self.pick_button.connect("color-selected", self.on_magnifier_color_selected)
        left_col.append(self.pick_button)

        self.color_preview = ColorPreview()
        self.color_preview.set_size_request(100, -1)
        self.color_preview.connect("similar_color_selected", self.on_similar_color_selected)
        left_col.append(self.color_preview)

        self.history_bar = HistoryBar()
        self.history_bar.connect("color-selected", self.on_history_color_selected)
        right_col.append(self.history_bar)
        
        self.color_values = ColorValues()
        right_col.append(self.color_values)


    # start searching for a color to pick traveling the mouse
    def on_start_pick_mode(self, button):
        if self.picking:
            return

        self.magnifier.start()
        self.picking = True
        self.pick_button.set_text("Release")
        self.set_picker_cursor()


    # pick color from the pixel under the mouse
    def on_stop_pick_mode(self, button):
        if not self.picking:
            return
        
        self.magnifier.stop()
        self.picking = False
        self.pick_button.set_text("Pick color")
        self.reset_cursor()


    def on_magnifier_aborted(self, button):
        print("on_magnifier_aborted")

        self.magnifier.stop()
        self.picking = False
        self.pick_button.set_text("Pick color")
        self.reset_cursor()

        
    # actions to take after a new color is picked from the magnifier
    def on_magnifier_color_selected(self, button):
        color = self.magnifier.current_color
        self.color_preview.set_color(color)
        self.color_values.set_color(color)
        self.history_bar.add_color(color)


    # actions to take after a color is picked from the history
    def on_history_color_selected(self, widget, color):
        self.color_preview.set_color(color)
        self.color_values.set_color(color)


    # actions to take after a similar color is picked from the preview
    def on_similar_color_selected(self, widget, color):
        self.color_preview.set_color(color)
        self.color_values.set_color(color)

        # add the color in history only if its not the same with the last one to avoid some replications
        last_color = self.history_bar.last_color
        if color.hex != last_color.hex:
            self.history_bar.add_color(color)


    # change the cursor icon to pick color icon
    def set_picker_cursor(self):
        surface = self.get_surface()
        if not surface:
            return

        cursor = Gdk.Cursor.new_from_name("crosshair")
        surface.set_cursor(cursor)
    
    
    # set the cursor icon to the default
    def reset_cursor(self):
        surface = self.get_surface()
        if surface:
            surface.set_cursor(None)


