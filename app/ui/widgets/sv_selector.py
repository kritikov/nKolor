import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject
from app.utils.color import Color
from app.ui.widgets.crosshair import Crosshair
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

        # Surface for gradient
        self.sv_surface = None

        # Drawing area
        self.darea = Gtk.DrawingArea()
        self.darea.set_content_width(width)
        self.darea.set_content_height(height)
        self.darea.set_draw_func(self.on_draw)
        self.set_child(self.darea)

        # Crosshair
        self.crosshair = Crosshair()
        self.crosshair.set_can_target(False)
        self.add_overlay(self.crosshair)
        self.update_crosshair_position()

        # Drag gesture
        self.drag = Gtk.GestureDrag()
        self.drag.connect("drag-begin", self.on_drag_begin)
        self.drag.connect("drag-update", self.on_drag_update)
        self.darea.add_controller(self.drag)

        # Build initial surface
        self.rebuild_surface()

    # ----------------- Drawing -----------------
    def on_draw(self, area, cr, width, height):
        if self.sv_surface:
            cr.set_source_surface(self.sv_surface, 0, 0)
            cr.paint()

    def rebuild_surface(self):
        """Rebuild the SV surface based on the current hue."""
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
        self.darea.queue_draw()

    # ----------------- Crosshair -----------------
    def update_crosshair_position(self):
        x = self.saturation * self.width
        y = (1.0 - self.value) * self.height
        self.crosshair.set_position(x, y)
        self.crosshair.queue_draw()

    # ----------------- Drag -----------------
    def on_drag_begin(self, gesture, start_x, start_y):
        self.drag_start_x = start_x
        self.drag_start_y = start_y
        self.update_from_position(start_x, start_y)

    def on_drag_update(self, gesture, offset_x, offset_y):
        abs_x = self.drag_start_x + offset_x
        abs_y = self.drag_start_y + offset_y
        self.update_from_position(abs_x, abs_y)

    def update_from_position(self, x, y):
        x = max(0, min(x, self.width))
        y = max(0, min(y, self.height))

        self.saturation = x / self.width
        self.value = 1.0 - (y / self.height)

        self.update_crosshair_position()
        self.emit("sv-changed", self.saturation, self.value)

    # ----------------- Public -----------------
    def set_hue(self, hue: float):
        self.hue = hue
        self.rebuild_surface()
        self.update_crosshair_position()

    def set_sv(self, s: float, v: float):
        self.saturation = s
        self.value = v
        self.update_crosshair_position()
