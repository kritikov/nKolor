import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GObject
from nKolor.utils.color import Color
from nKolor.ui.widgets.crosshair import Crosshair
import cairo

class SVSelector(Gtk.Overlay):
    __gsignals__ = {
        "sv-changed": (GObject.SignalFlags.RUN_FIRST, None, (float, float)),  # saturation, value
    }

    def __init__(self, width=256, height=256, hue=0.0, saturation=0.0, value=1.0):
        super().__init__()

        self.set_size_request(width, height)
        self.width = width
        self.height = height
        self.hue = hue
        self.saturation = saturation
        self.value = value
        
        self.build_ui()

    def build_ui(self)->None:

        # Surface for gradient
        self.sv_surface = None

        # Drawing area
        self.colors_area = Gtk.DrawingArea()
        self.colors_area.set_content_width(self.width)
        self.colors_area.set_content_height(self.height)
        self.colors_area.set_draw_func(self.on_draw)
        self.colors_area.set_focusable(True)
        self.colors_area.add_css_class("focusable-widget")
        self.set_child(self.colors_area)
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.colors_area.add_controller(key_controller)

        # Crosshair
        self.crosshair = Crosshair()
        self.crosshair.set_can_target(False)
        self.add_overlay(self.crosshair)
        self.update_crosshair_position()

        # Drag gesture
        self.drag = Gtk.GestureDrag()
        self.drag.connect("drag-begin", self.on_drag_begin)
        self.drag.connect("drag-update", self.on_drag_update)
        self.colors_area.add_controller(self.drag)

        # Build initial surface
        self.rebuild_surface()


    def on_drag_begin(self, gesture, start_x, start_y)-> None:
        self.colors_area.grab_focus()
        self.drag_start_x = start_x
        self.drag_start_y = start_y
        self.update_color_from_sv_position(start_x, start_y)


    def on_drag_update(self, gesture, offset_x, offset_y)-> None:
        abs_x = self.drag_start_x + offset_x
        abs_y = self.drag_start_y + offset_y
        self.update_color_from_sv_position(abs_x, abs_y)


    # move the pointer in the colors area using the keyboard
    def on_key_pressed(self, controller, keyval, keycode, state)-> None:
        step = 0.01  

        if keyval == Gdk.KEY_Left:
            self.saturation = max(0.0, self.saturation - step)
        elif keyval == Gdk.KEY_Right:
            self.saturation = min(1.0, self.saturation + step)
        elif keyval == Gdk.KEY_Up:
            self.value = min(1.0, self.value + step)
        elif keyval == Gdk.KEY_Down:
            self.value = max(0.0, self.value - step)
        else:
            return False 

        self.update_crosshair_position()
        self.emit("sv-changed", self.saturation, self.value)
        return True  


    # the drawing function of the colors area
    def on_draw(self, area, cr, width:int, height:int)-> None:
        if self.sv_surface:
            cr.set_source_surface(self.sv_surface, 0, 0)
            cr.paint()


   # Rebuild the SV surface based on the current hue
    def rebuild_surface(self)-> None:
        w, h = self.width, self.height
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
        cr = cairo.Context(surface)

        # Saturation gradient (left=white, right=hue color)
        r, g, b = Color.hsv_to_rgb_normalized(self.hue, 1, 1)
        sat_grad = cairo.LinearGradient(0, 0, w, 0)
        sat_grad.add_color_stop_rgb(0, 1, 1, 1)   # S=0 → white
        sat_grad.add_color_stop_rgb(1, r, g, b)   # S=1 → hue
        cr.set_source(sat_grad)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        # Value gradient (top=transparent, bottom=black)
        val_grad = cairo.LinearGradient(0, 0, 0, h)
        val_grad.add_color_stop_rgba(0, 0, 0, 0, 0)   # V=1 (top)
        val_grad.add_color_stop_rgba(1, 0, 0, 0, 1)   # V=0 (bottom)
        cr.set_source(val_grad)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        self.sv_surface = surface
        self.colors_area.queue_draw()


    # update the pointer position
    def update_crosshair_position(self)-> None:
        x = self.saturation * self.width
        y = (1.0 - self.value) * self.height
        self.crosshair.set_position(x, y)
        self.crosshair.queue_draw()


    # update the color from the coordinates
    def update_color_from_sv_position(self, x:float, y:float)-> None:
        x = max(0, min(x, self.width))
        y = max(0, min(y, self.height))

        self.saturation = x / self.width
        self.value = 1.0 - (y / self.height)

        self.update_crosshair_position()
        self.emit("sv-changed", self.saturation, self.value)

    
    # update the widget setting the hue       
    def set_hue(self, hue: float)-> None:
        self.hue = hue
        self.rebuild_surface()
        self.update_crosshair_position()


    # update the widget setting the saturation and the value  
    def set_sv(self, s: float, v: float)-> None:
        self.saturation = s
        self.value = v
        self.update_crosshair_position()
