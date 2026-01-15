import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GObject
from nKolor.utils.color import Color

class HueSlider(Gtk.DrawingArea):

    __gsignals__ = {
            "hue_changed": (GObject.SignalFlags.RUN_FIRST, None, (float,)),
        }
 
    def __init__(self, width=30, height=256, initial_hue=0.0):
        super().__init__()

        self.hue = initial_hue  # 0..1
        self.height = height

        self.build_ui(width, height)
       

    def build_ui(self, width: int, height: int) -> None:

         # drawing area with the colors
        self.set_content_width(width)
        self.set_content_height(height)
        self.set_focusable(True)    
        self.set_can_focus(True)
        self.add_css_class("focusable-widget")

        self.set_draw_func(self.draw_colors_area)

        # --- Click gesture ---
        click = Gtk.GestureClick()
        click.connect("pressed", self.on_mouse_pressed)
        self.add_controller(click)

        # --- Drag gesture ---
        drag = Gtk.GestureDrag()
        drag.connect("drag-update", self.on_drag_update)
        self.add_controller(drag)

        # --- Keyboard gesture ---
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)


     # drawing function for the colors area
    def draw_colors_area(self, area, cr, width: int, height: int)->None:
        for y in range(height):
            h = y / height
            r, g, b = Color.hsv_to_rgb_normalized(h, 1.0, 1.0)
            cr.set_source_rgb(r, g, b)
            cr.rectangle(0, y, width, 1)
            cr.fill()

        self.draw_pointer(cr, width, height)


    # draw a pointer on the colors area corresponding to the selected hue
    def draw_pointer(self, cr, width: int, height: int)->None:
        indicator_y = self.hue * height
        arrow_size = 12
        arrow_width = min(arrow_size, width / 2)

        cr.set_source_rgb(0, 0, 0)  # λευκό
        cr.move_to(width - arrow_width, indicator_y)     # κορυφή
        cr.line_to(width, indicator_y - arrow_width / 2)
        cr.line_to(width, indicator_y + arrow_width / 2)
        cr.close_path()
        cr.fill()


    # update the hue from the height if the scale
    def update_hue_from_y(self, y: float):
        height = self.get_allocated_height()
        if height <= 0:
            return
        self.set_hue(y / height)


    # set the hue from a value
    def set_hue(self, hue: float):
        self.hue = max(0.0, min(1.0, hue))
        self.queue_draw()
        self.emit("hue_changed", self.hue)


    def on_mouse_pressed(self, gesture, n_press, x, y):
        self.grab_focus()
        self.update_hue_from_y(y)


    def on_drag_update(self, gesture, dx, dy):
        success, x, y = gesture.get_point()
        if not success:
            return
        self.update_hue_from_y(y)


    def on_key_pressed(self, controller, keyval, keycode, state):
        small_step = 0.005 
        page_step = 0.05

        if keyval == Gdk.KEY_Up:
            self.set_hue(self.hue - small_step)
            return True

        if keyval == Gdk.KEY_Down:
            self.set_hue(self.hue + small_step)
            return True

        if keyval == Gdk.KEY_Page_Up:
            self.set_hue(self.hue - page_step)
            return True

        if keyval == Gdk.KEY_Page_Down:
            self.set_hue(self.hue + page_step)
            return True

        return False


    
