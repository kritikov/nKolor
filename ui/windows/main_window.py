import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk, Gio
from nKolor.ui.widgets.history_bar import HistoryBar
from nKolor.ui.widgets.pick_button import PickButton
from nKolor.ui.widgets.color_preview import ColorPreview
from nKolor.ui.widgets.color_values import ColorValues
from nKolor.utils.color import Color
from nKolor.ui.windows.magnifier_window import MagnifierWindow
from nKolor.ui.windows.hex_editor_window import HexEditorWindow
from nKolor.ui.windows.rgb_editor_window import RgbEditorWindow
from nKolor.ui.windows.hsl_editor_window import HslEditorWindow
from nKolor.ui.windows.hsv_editor_window import HsvEditorWindow
from nKolor.ui.windows.hsv_picker_window import HSVPickerWindow
from nKolor.ui.windows.about_window import AboutWindow
from nKolor.resources.resources import Resources


class MainWindow(Gtk.ApplicationWindow) : 

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app)
        
        self.set_title("nKolor")
        self.set_default_size(520, 220)
        self.set_resizable(False) 
        self.current_color = Color(50, 180, 150) # initial color
        self.magnifier = MagnifierWindow()

        self.build_ui()

        # Key controller για ESC
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)


    def build_ui(self) -> None:
        root_child = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=10)
        root_child.add_css_class("window-root-child")
        self.set_child(root_child)  

        # general cοnstruction
        first_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        second_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        third_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        right_col = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=12)
        second_row.append(left_col)
        second_row.append(right_col)
        root_child.append(first_row)
        root_child.append(second_row)
        root_child.append(third_row)

        # info button
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        first_row.append(spacer)
        info_btn = Gtk.Button()
        info_btn.add_css_class("info-button")
        info_btn.set_cursor(Gdk.Cursor.new_from_name("pointer"))
        info_icon = Gtk.Image.new_from_file(Resources.icon("info.png"))
        info_btn.set_child(info_icon)
        info_btn.set_tooltip_text("about the nKolor")
        info_btn.connect("clicked", self.open_about_window)
        first_row.append(info_btn)

        # elements
        left_col_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        left_col.append(left_col_buttons)

        pick_button = PickButton()
        pick_button.connect("start", self.on_start_pick_mode)
        pick_button.connect("stop", self.on_stop_pick_mode)
        pick_button.connect("aborted", self.on_magnifier_aborted)
        left_col_buttons.append(pick_button)

        hsv_selector_btn = Gtk.Button()
        hsv_selector_btn.add_css_class("icon-button") 
        hsv_selector_btn.set_cursor(Gdk.Cursor.new_from_name("pointer")) 
        hsv_selector_icon = Gtk.Image.new_from_file(Resources.icon("color-wheel.png"))
        hsv_selector_btn.set_child(hsv_selector_icon);
        hsv_selector_btn.set_tooltip_text("select from HSV picker")
        hsv_selector_btn.connect("clicked", self.open_hsv_selector)
        left_col_buttons.append(hsv_selector_btn)

        self.color_preview = ColorPreview()
        self.color_preview.set_size_request(100, -1)
        self.color_preview.connect("similar_color_selected", self.on_similar_color_selected)
        self.color_preview.set_color(self.current_color)
        left_col.append(self.color_preview)
        
        self.color_values = ColorValues()
        self.color_values.connect("edit_hex", self.on_edit_hex)
        self.color_values.connect("edit_rgb", self.on_edit_rgb)
        self.color_values.connect("edit_hsl", self.on_edit_hsl)
        self.color_values.connect("edit_hsv", self.on_edit_hsv)
        self.color_values.set_color(self.current_color)
        right_col.append(self.color_values)

        self.history_bar = HistoryBar()
        self.history_bar.connect("color-selected", self.on_history_color_selected)
        third_row.append(self.history_bar)


    # start searching for a color to pick traveling the mouse
    def on_start_pick_mode(self, widget) -> None:
        self.magnifier.start()
        self.set_picker_cursor()

        
    # actions to take after a new color is picked from the magnifier
    def on_stop_pick_mode(self, widget) -> None:
        self.magnifier.stop()
        self.reset_cursor()
        self.current_color = self.magnifier.current_color
        self.color_preview.set_color(self.current_color)
        self.color_values.set_color(self.current_color)
        self.history_bar.add_color(self.current_color)


    # actions to take after the magnifier is closed without picking a color
    def on_magnifier_aborted(self, widget) -> None:
        self.magnifier.stop()
        self.reset_cursor()

 
    # actions to take after a color is picked from the history
    def on_history_color_selected(self, widget, color:Color) -> None:
        self.current_color = color
        self.color_preview.set_color(self.current_color)
        self.color_values.set_color(self.current_color)


    # actions to take after a similar color is picked from the preview
    def on_similar_color_selected(self, widget, color:Color) -> None:
        self.current_color = color
        self.color_preview.set_color(self.current_color)
        self.color_values.set_color(self.current_color)

        # add the color in history only if its not the same with the last one to avoid some replications
        last_color = self.history_bar.last_color
        if last_color == None or self.current_color != last_color: 
            self.history_bar.add_color(color)


    # actions to take after a color is updated from the RGB editor
    def on_color_edited(self, widget, color:Color) -> None:
        self.current_color = color.copy()
        self.color_preview.set_color(self.current_color)
        self.color_values.set_color(self.current_color)
        self.history_bar.add_color(self.current_color)


    # change the cursor icon to pick color icon
    def set_picker_cursor(self) -> None:
        surface = self.get_surface()
        if not surface:
            return

        cursor = Gdk.Cursor.new_from_name("crosshair")
        surface.set_cursor(cursor)
    
    
    # set the cursor icon to the default
    def reset_cursor(self) -> None:
        surface = self.get_surface()
        if surface:
            surface.set_cursor(None)


    # open the hex editor to edit the color
    def on_edit_hex(self, widget) -> None:
        win = HexEditorWindow(self.get_application(), self.current_color)
        self.open_color_editor(win)

    # open the rgb editor to edit the color
    def on_edit_rgb(self, widget) -> None:
        win = RgbEditorWindow(self.get_application(), self.current_color)
        self.open_color_editor(win)

    # open the hsl editor to edit the color
    def on_edit_hsl(self, widget) -> None:
        win = HslEditorWindow(self.get_application(), self.current_color)
        self.open_color_editor(win)

    # open the hsv editor to edit the color
    def on_edit_hsv(self, widget) -> None:
        win = HsvEditorWindow(self.get_application(), self.current_color)
        self.open_color_editor(win)


    # open a color editor
    def open_color_editor(self, editor) -> None:
        editor.connect("color_selected", self.on_color_edited)  
        editor.set_transient_for(self)
        editor.set_modal(True)
        editor.set_destroy_with_parent(True)
        editor.present()


    # open the hsv color picker
    def open_hsv_selector(self, widget) -> None:
        win = HSVPickerWindow(self.get_application(), self.current_color)
        win.connect("color_selected", self.on_color_edited)
        win.set_transient_for(self)
        win.set_modal(True)
        win.set_destroy_with_parent(True)
        win.present()
    
    # open the abοut window
    def open_about_window(self, action):
        win = AboutWindow(self.get_application())
        win.set_transient_for(self)
        win.set_modal(True)
        win.set_destroy_with_parent(True)
        win.present()

    # close the app when ESC is pressed
    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.close()
            return True
        return False