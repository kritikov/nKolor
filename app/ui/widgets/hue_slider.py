import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject
from app.utils.color import Color
import colorsys, cairo

class HueSlider(Gtk.Box):

    __gsignals__ = {
            "hue_changed": (GObject.SignalFlags.RUN_FIRST, None, (float,)),
        }
 
    def __init__(self, width=30, height=256, initial_hue=0.0):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)

        self.hue = initial_hue  # 0..1
        self.is_dragging = False

        self.build_ui(width, height)
       

    def build_ui(self, width: int, height: int) -> None:

         # drawing area with the colors
        self.colors_area = Gtk.DrawingArea()
        self.colors_area.set_content_width(width)
        self.colors_area.set_content_height(height)
        self.colors_area.set_draw_func(self.draw_colors_area)
        self.append(self.colors_area)

        # slider to choose color
        adjustment = Gtk.Adjustment(
            value=self.hue,
            lower=0.0,
            upper=1.0,
            step_increment=0.001,
            page_increment=0.01,
            page_size=0.0,
        )
        self.scale = Gtk.Scale(
            orientation=Gtk.Orientation.VERTICAL,
            adjustment=adjustment,
        )
        self.scale.set_draw_value(False)
        self.scale.connect("value-changed", self.on_scale_changed)
        self.append(self.scale)


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


    # slider event 
    def on_scale_changed(self, scale):
        self.hue = scale.get_value()
        self.colors_area.queue_draw()
        self.emit("hue_changed", self.hue)


